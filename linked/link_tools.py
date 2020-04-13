from .models import Link, Review, Category


def view_final_link_dict(link: Link, reviews: [Review], average: float, total_reviews: int) -> dict:
    final_dict = {'link': link, 'reviews': reviews, 'ave': average, 'total_reviews': total_reviews}

    return final_dict


def final_link_review_calc_dict(link: Link, reviews: [Review], average, total_reviews: int) -> dict:
    final_dict = {'link': link, 'reviews': reviews, 'average': average, 'total': total_reviews}
    return final_dict


def view_final_cat_link_dict(category: Category, link_dict: [dict]) -> dict:
    final_dict = {'category': category, 'links': link_dict}

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
    print("LEN: " + str(len(links)))
    for i in range(len(links)):
        final.append((links[i], links[i].name))
        # links[i]['reviews'] = reviews
        # print(links[i]['reviews'])

    return final
