import os
import os.path
import yaml


def extract_front_matter(fullpath):
    with open(fullpath, 'r', encoding='utf8') as f:
        return next(yaml.safe_load_all(f))


def create_category_page(category, config):
    fullpath = os.path.join('_category', category + '.md')
    if os.path.isfile(fullpath):
        return

    try:
        category_config = config['categories'][category]
    except:
        category_config = {}

    try:
        title = category_config['title']
    except:
        title = category.title().replace('-', ' ')

    try:
        description = category_config['description']
    except:
        description = ''

    with open(fullpath, 'w', encoding='utf8') as f:
        f.write('---\n')
        f.write('layout: category\n')
        f.write(f'category: {category}\n')
        f.write(f'title: {title}\n')
        for key in category_config.keys():
            if not key in ['title', 'description']:
                f.write(f'{key}: {category_config[key]}\n')
        f.write('---\n\n')
        f.write(description)
        f.write('\n')


def create_tag_page(tag, config):
    normalized_tag = tag.replace(
        ' ', '-').lower().replace('.net', '-dot-net').replace('.', '-')
    if normalized_tag.startswith('-'):
        normalized_tag = normalized_tag[1:]

    fullpath = os.path.join('_tag', normalized_tag + '.md')
    if os.path.isfile(fullpath):
        return

    with open(fullpath, 'w', encoding='utf8') as f:
        f.write('---\n')
        f.write('layout: tag\n')
        f.write(f'normalized_tag: {normalized_tag}\n')
        f.write(f'tag: {tag}\n')
        f.write('---\n')


def main():
    with open('_config.yml', 'r', encoding='utf8') as f:
        config = yaml.safe_load(f)

    fullpaths = [
        os.path.join(root, p)
        for root, dirs, files in os.walk('_posts')
        for p in files
    ]

    for p in fullpaths:
        front_matter = extract_front_matter(p)
        categories = front_matter['categories']
        for category in categories:
            create_category_page(category, config)
        tags = front_matter['tags']
        for tag in tags:
            create_tag_page(tag, config)


if __name__ == "__main__":
    main()
