import pandas as pd


def biomass_to_mtc02(layer):
    layer.emissions.SUM = layer.emissions.SUM.astype(float)
    layer.emissions['emissions_mtc02'] = layer.emissions.SUM * 3.67 * .5 / 1000000

    del layer.emissions['emissions']

    return layer.emissions


def value_to_tcd_year(value):

    remap_dict = {
        1: [{'tcd': '1-10 %', 'sub': 40}],
        2: [{'tcd': '11-15 %', 'sub': 60}],
        3: [{'tcd': '16-20 %', 'sub': 80}],
        4: [{'tcd': '21-25 %', 'sub': 100}],
        5: [{'tcd': '26-30 %', 'sub': 120}],
        6: [{'tcd': '31-50 %', 'sub': 140}],
        7: [{'tcd': '51-75 %', 'sub': 160}],
        8: [{'tcd': '76-100 %', 'sub': 180}]
    }
    # divide the coded value by interval. if its 1.175, use int to get 1
    div = int(value / 40)

    # look up that value to get TCD
    tcd = remap_dict[div][0]['tcd']

    # find this value which is subtraced from the coded value. 47-40 = 7. Gets the year
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
        for key, value in mydict[intersect_filename].items():
            id_num = key
        for key, value in mydict.items():

            for i in range(0, id_num + 1):
                try:
                    columns_to_add.append(mydict[key][i])

                except KeyError:
                    pass

    except KeyError:
        pass

    return columns_to_add
