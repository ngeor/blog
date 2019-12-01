import argparse
import os
import os.path
import yaml


def create_category_page(category, config, args):
    '''
    Creates a category page.

    :param category: The URL segment of the category
    '''
    fullpath = os.path.join('_category', category + '.md')
    if os.path.isfile(fullpath) and not args.overwrite:
        return

    # Get the category configuration
    try:
        category_config = config['categories'][category]
    except:
        category_config = {}

    # Create the category title
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
        f.write(f'url_segment: {category}\n')
        f.write(f'title: {title}\n')
        for key in category_config.keys():
            if not key in ['title', 'description']:
                f.write(f'{key}: {category_config[key]}\n')
        f.write('---\n\n')
        f.write(description)
        f.write('\n')


def create_tag_page(tag, config, args):
    '''
    Creates a tag page.

    :param tag: The human friendly name of the tag (i.e. not the URL segment)
    '''
    normalized_tag = tag.replace(
        ' ', '-').lower().replace('.net', '-dot-net').replace('.', '-').replace('#', '-sharp').replace('++', '-plus-plus')
    if normalized_tag.startswith('-'):
        normalized_tag = normalized_tag[1:]

    fullpath = os.path.join('_tag', normalized_tag + '.md')
    if os.path.isfile(fullpath) and not args.overwrite:
        return

    with open(fullpath, 'w', encoding='utf8') as f:
        f.write('---\n')
        f.write('layout: tag\n')
        f.write(f'url_segment: {normalized_tag}\n')
        f.write(f'title: {tag}\n')
        f.write('---\n')


def extract_front_matter(fullpath):
    with open(fullpath, 'r', encoding='utf8') as f:
        return next(yaml.safe_load_all(f))


def process_post(fullpath, config, args):
    front_matter = extract_front_matter(fullpath)
    categories = front_matter['categories']
    for category in categories:
        create_category_page(category, config, args)
    tags = front_matter['tags']
    for tag in tags:
        create_tag_page(tag, config, args)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Preprocess category and tag pages")
    parser.add_argument(
        "--overwrite", help="Overwrite existing files", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    with open('_config.yml', 'r', encoding='utf8') as f:
        config = yaml.safe_load(f)

    fullpaths = [
        os.path.join(root, p)
        for root, dirs, files in os.walk('_posts')
        for p in files
    ]

    for post_fullpath in fullpaths:
        process_post(post_fullpath, config, args)


if __name__ == "__main__":
    main()
