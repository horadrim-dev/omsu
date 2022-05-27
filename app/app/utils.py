import os

# функция обработки файлов при загрузке
def get_filename(filename, request):
    return filename.lower()

def slugify_rus(s:str):
    '''функция траслитерации строки на кириллице'''
    from django.template.defaultfilters import slugify as django_slugify

    alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
                'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
                'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sh', 'ы': 'y', 'э': 'e', 'ю': 'yu',
                'я': 'ya'}

    def slugify(s):
        """
        Overriding django slugify that allows to use russian words as well.
        """
        return django_slugify(''.join(alphabet.get(w, w) for w in s.lower()))

    return slugify(s)


def remove_empty_dirs(path_to_dir:str):
    '''Рекурсивно обходит папки по заданному path и удаляет пустые
    пока не встретит НЕ пустую'''
    if os.path.exists(path_to_dir):
        if not os.listdir(path_to_dir): # проверяем что папка пуста
            os.rmdir(path_to_dir) # удаляем
            remove_empty_dirs(os.path.split(path_to_dir[:-1])[0])
        else:
            return False
    else:
        raise NotADirectoryError