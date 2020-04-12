from .models import Link, Review, Category


def view_final_link_dict(link: Link, reviews: [Review]) -> dict :
    final_dict = {}

    final_dict['link'] = link
    final_dict['reviews'] = reviews

    return final_dict


def retrieve_categories_as_list_of_tuples():
    # categories = Category.objects.order_by('name')[:]
    # print("LEN: " + len(categories))
    # print("==============================================================")
    # CATEGORIES = []
    # print("LEN: " + len(categories))
    # for (i in range(len(categories))):
    #     CATEGORIES.append(categories[i].pk, categories[i].name)

    links = Category.objects.order_by('name')[:]

    final = []

    final.append((-1, "Select a category"))

    for i in range(len(links)):
        final.append((links[i], links[i].name))
        # links[i]['reviews'] = reviews
        # print(links[i]['reviews'])

    return final