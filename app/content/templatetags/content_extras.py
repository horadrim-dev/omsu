from django import template
import math

register = template.Library()

def chunks_generator(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]

@register.simple_tag()
def split_posts_by_columns(posts, num_columns, sort_direction='horizontal'):
    '''
    Разбивает (упорядоченный по дате) список объектов по колонкам так, чтобы
    первые элементы списка были первыми в колонках
    '''
    posts_by_columns = []
    max_posts =  calc_max_posts_in_col(posts, num_columns)
    if sort_direction == 'horizontal':
        for col in range(num_columns):
            posts_by_columns.append(
                posts[col::num_columns]
            )
    elif sort_direction == 'vertical':
        posts_by_columns = list(chunks_generator(posts, max_posts))

    return posts_by_columns

@register.simple_tag()
def calc_max_posts_in_col(posts, num_columns):
    return math.ceil(len(posts) // num_columns)


@register.simple_tag()
def posts_by_columns_flatten(posts_by_columns):
    '''
    Формирует одноуровневый массив объектов из ранее разбитого по колонкам
    (используется для получения списка постов, расположенных в новом порядке)
    '''
    return [post for posts in posts_by_columns for post in posts]
