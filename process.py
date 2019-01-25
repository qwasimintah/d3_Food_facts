import pandas as pd
import json


countries = pd.read_csv('tsv/products_countries.tsv', sep='\t')
categories = pd.read_csv('tsv/products_categories_min.tsv', sep='\t')
products = pd.read_csv('tsv/products.tsv', sep='\t')

combined = pd.merge(left = products, right = categories, on='code' )
combined = pd.merge(left=combined, right=countries, on='code')

def get_top_countries(df,food_type, top=10):
    
    return list(df.groupby('country')[food_type].sum().sort_values( ascending=False).index)[:top]


def get_top_values(df, food_type, top=10):
    
    return list(df.groupby('country')[food_type].sum().sort_values( ascending=False))[:top]


def get_ingredient_data(data, ing):
    return combined.groupby(['country','category'])[ing, 'category', 'country'].sum().sort_values(by=ing, ascending=False)
    



def get_plot_format_data(combined,ing, blue):
    country_list = get_top_countries(combined, ing)
    value_list = get_top_values(combined, ing)
    #print(value_list)
    details={}
    for country in country_list:
        if country not in details.keys():
            details[country]=[]
        other =0
        for value in blue.index:
            
            if country == value[0]:
                if len(details[country])<6:
                    details[country].append({value[1]:blue.loc[value][ing]})
                else:
                    other += blue.loc[value][ing]

        details[country].append({'other':other})

    result =[]
    counter = 0
    for key, value in details.items():
        freq_dict ={}
        legend={}
        for i, dt in enumerate(value):
            name = 'cat'+str(i+1)
            for x in  list(dt.keys()):
                legend[name] = truncate_long_cats(x)
            freq_dict[name] = list(dt.values())[0]
        #print(value_list[counter])
        result.append({"State": key, 'total':value_list[counter], "freq":freq_dict  , "legend": legend})
        counter+=1
    return result
                

def truncate_long_cats(cats):
    
    c = cats.split("-")
    if len(c)>2:
        c = [c[0], c[-1]]
        res= "...".join(c)
    else:
        res = "-".join(c)
    return res[:15]

# list the integredients available

ingredients = ['alcohol_100g', 'sugars_100g', 'salt_100g', 'cholesterol_100g', 'fruits-vegetables-nuts_100g']
final = {}
for ing in ingredients:
    blue = get_ingredient_data(combined, ing)
    data = get_plot_format_data(combined,ing, blue)
    
    final[ing.split('_')[0]]= data


# save json


with open('final4.json','w') as f:
    json.dump(final, f)
