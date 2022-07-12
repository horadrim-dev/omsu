from django import template
import math

register = template.Library()

# def chunks_generator(lst, n):
#     for i in range(0, len(lst), n):
#         yield lst[i : i + n]

# def chunks_generator(lst, n):
#     for i in range(0, len(lst), n):
#         yield lst[i : i + n]

@register.simple_tag()
def split_posts_by_columns(posts, num_columns):
    '''
    Разбивает (упорядоченный по дате) список по колонкам так, чтобы
    первые элементы списка были первыми в колонках
    '''
    posts_by_columns = []
    for col in range(num_columns):
        posts_by_columns.append(
            posts[col::num_columns]
        )
    return posts_by_columns