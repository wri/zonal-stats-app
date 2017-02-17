import pandas as pd


def process_emissions(layer):

    minmax = pd.concat([layer.emissions_min_of, layer.emissions_max_of])
    idx = ['VALUE', 'ID']
    joined = minmax.set_index(idx).join(layer.forest_loss.set_index(idx), lsuffix='_bio', rsuffix='_loss')

    joined['bio_per_pix'] = joined.SUM_bio * joined.SUM_loss / 10000
    joined = joined.reset_index()

    avg_bio = joined.groupby(['VALUE', 'ID', 'SUM_loss'])['bio_per_pix'].mean()
    avg_bio = avg_bio.to_frame().reset_index()
    avg_bio['emissions'] = avg_bio.bio_per_pix * 3.67 * .5
    del avg_bio['bio_per_pix']

    return avg_bio


def value_to_tcd_year(value):

    remap_dict = {
        1: [{'tcd': '1-10 %', 'sub': 20}],
        2: [{'tcd': '11-15 %', 'sub': 40}],
        3: [{'tcd': '16-20 %', 'sub': 60}],
        4: [{'tcd': '21-25 %', 'sub': 80}],
        5: [{'tcd': '26-30 %', 'sub': 100}],
        6: [{'tcd': '31-50 %', 'sub': 120}],
        7: [{'tcd': '51-75 %', 'sub': 140}],
        8: [{'tcd': '76-100 %', 'sub': 160}]
    }

    div = int(value/20)
    tcd = remap_dict[div][0]['tcd']

    sub = remap_dict[div][0]['sub']

    year = 2000 + (value - sub)

    if year == 2000:
        year = "no loss"

    return tcd, year


def generate_list_columns(intersect, intersect_col):

    columns_to_add = []
    if len(intersect_col) > 0:

        columns_to_add.append(intersect_col)

    intersect_filename = intersect.split('\\')[-1]
    admin_dict = [{'adm0': {1: "ISO"}, 'adm1': {2: "ID_1"}, 'adm2': {3: "ID_2"}, 'adm3': {4: "ID_3"},
                   'adm4': {5: "ID_4"}, 'adm5': {6: "ID_5"}}]
    
    mydict = admin_dict[0]
    try:
        # incrementally add all admin levels for whatever admin level is intersected.
        # example: adm2 will ad id_2, id_1, iso
        for key, value in mydict[intersect_filename].iteritems():
            id_num = key
        for key, value in mydict.iteritems():

            for i in range(0, id_num + 1):
                try:
                    columns_to_add.append(mydict[key][i])

                except KeyError:
                    pass

    except KeyError:
        pass

    return columns_to_add
