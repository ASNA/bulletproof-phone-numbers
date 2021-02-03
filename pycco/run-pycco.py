# Generate AVR annotated code.

# The modified Pycco Python file is here:
# C:\Users\roger\AppData\Local\Programs\Python\Python38\Lib\site-packages\pycco\main.py

import glob, os, shutil, re

def create_index_file(template_filename, files):
    template_contents = read_file(template_filename)
    index_list = create_index_list(files)
    template_contents = template_contents.replace('{{directory}}', index_list)
    write_file('./pycco-docs/master_index.html', template_contents)

def write_file(filename, contents):
    with open(filename, 'w', encoding="utf-8") as f:
        f.write(contents)

def read_file(filename):
    with open(filename, 'r', encoding="utf-8") as f:
        return f.read()

def delete_folder_contents(folder):
    #  Save template file contents.
    directory_template_contents = read_file('./pycco-docs/__index.template.html')

    for root, dirs, files in os.walk(folder):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
    # Restore template file contents.
    write_file('./pycco-docs/__index.template.html', directory_template_contents)            

def create_index_list(files):
    index_list = ''
    anchor_tags = []
    template = '{filename}|<li><a href="{url}">{filename}</a></li>'
    root_name = ''
    for file in files:
        if '\\' in file:
            root_name = ''
        else:            
            root_name = '_ROOT_/'
        filename_to_show = root_name + file.replace('\\', '/').lower()
        file_without_extension = file.replace('.vr', '')
        tag = template.format(url=file_without_extension + '.html', filename=filename_to_show)
        anchor_tags.append(tag)
    anchor_tags.sort()

    for anchor_tag in anchor_tags:
        anchor_tag = anchor_tag.replace('_ROOT_/', '')
        index_list += re.sub(r'^.*\|', '', anchor_tag)

    return index_list
    
if __name__ == '__main__':  
    if not os.path.isdir('../pycco-docs'):    
        os.mkdir('../pycco-docs')        
    if not os.path.isfile('../pycco-docs/__index.template.html'):
        shutil.copy('index.template.html', '../pycco-docs/__index.template.html')        

    # This program needs to run in the context of the root directory.
    os.chdir('..')
    
    # places to look for source files
    searches = ('global.asax', 'web.config', '*.aspx', '**/*.aspx', '*.vr', '**/*.vr', 'app_code/*.vr' )
    # source file ending names to ignore.
    ignored_files = ('^.*designer.vr', '^.*assemblyinfo.vr')        

    files = []
    for search in searches:
        files.extend(glob.glob(search, recursive=True)) 

    purged_files = []
    for file in files:
        include_file = True
        for ignored_file in ignored_files:
            pattern = re.compile(ignored_file + '$', re.I)
            if re.match(pattern, file):
                print(f'Ignored file = {file}')
                include_file = False
                break
        if include_file:
            purged_files.append(file)       

    delete_folder_contents('./pycco-docs')

    create_index_file(template_filename='./pycco-docs/__index.template.html', files=purged_files)

    for file in purged_files:
        print(file)
        cmd = f'pycco {file} -d ./pycco-docs -l javascript -p'
        os.system(cmd)

    shutil.copy("pycco/pycco.css", './pycco-docs/')    
