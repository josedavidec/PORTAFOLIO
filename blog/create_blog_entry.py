import os
from datetime import datetime

# Configuración
template_path = os.path.join(os.path.dirname(__file__), 'blog-entry-template.html')
output_dir = os.path.join(os.path.dirname(__file__), 'blog')
blog_index_path = os.path.join(os.path.dirname(__file__), '..', 'blog.html')
index_path = os.path.join(os.path.dirname(__file__), '..', 'index.html')

entry_title = input("Introduce el título de la nueva entrada: ")
entry_date_input = input("Introduce la fecha de la entrada (dd/mm/yyyy) (deja en blanco para usar la fecha actual): ")

# Usar la fecha actual si no se proporciona una fecha
if entry_date_input:
    entry_date = datetime.strptime(entry_date_input, "%d/%m/%Y").strftime("%d/%m/%Y")
else:
    entry_date = datetime.now().strftime("%d/%m/%Y")

entry_filename = entry_title.lower().replace(' ', '-').replace(':', '').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u') + '.html'
entry_image = input("Introduce la ruta de la imagen de la entrada (deja en blanco para usar la imagen por defecto): ")

# Usar una imagen por defecto si no se proporciona una ruta
if not entry_image:
    entry_image = 'images/default.jpg'

entry_content_input = input("Introduce el contenido de la entrada (deja en blanco para agregarlo más tarde): ")

# Usar un contenido por defecto si no se proporciona uno
if not entry_content_input:
    entry_content_input = 'Contenido completo de la entrada...'

# Crear la carpeta de salida si no existe
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Leer la plantilla
with open(template_path, 'r', encoding='utf-8') as file:
    template_content = file.read()

# Reemplazar el título, la fecha, la imagen y el contenido en la plantilla
entry_content = template_content.replace('Título de la Entrada', entry_title)
entry_content = entry_content.replace('Fecha: DD/MM/YYYY', f'Fecha: {entry_date}')
entry_content = entry_content.replace('images/blog-image.jpg', entry_image)
entry_content = entry_content.replace('Contenido completo de la entrada...', entry_content_input)

# Guardar la nueva entrada
output_path = os.path.join(output_dir, entry_filename)
with open(output_path, 'w', encoding='utf-8') as file:
    file.write(entry_content)

print(f'Nueva entrada creada: {output_path}')

# Generar el HTML de la nueva entrada
new_entry_html = f'''
<article class="blog-entry">
    <img src="{entry_image}" alt="Imagen de la {entry_title}">
    <div class="entry-content">
        <h3><a href="blog/{entry_filename}">{entry_title}</a></h3>
        <span class="entry-date">Fecha: {entry_date}</span>
    </div>
</article>
'''

def insert_entry_sorted(content, new_entry_html, entry_date):
    entries = content.split('<article class="blog-entry">')[1:]
    entries = [f'<article class="blog-entry">{entry}' for entry in entries]
    entries.append(new_entry_html)
    entries.sort(key=lambda x: datetime.strptime(x.split('Fecha: ')[1].split('</span>')[0], "%d/%m/%Y"), reverse=True)
    return '<div class="blog-entries">' + ''.join(entries[:3]) + '</div>'

def update_html_file(file_path, new_entry_html, entry_date):
    with open(file_path, 'r+', encoding='utf-8') as file:
        content = file.read()
        start_pos = content.find('<div class="blog-entries">')
        end_pos = content.find('</div>', start_pos) + len('</div>')
        entries_content = content[start_pos:end_pos]
        updated_entries_content = insert_entry_sorted(entries_content, new_entry_html, entry_date)
        updated_content = content[:start_pos] + updated_entries_content + content[end_pos:]
        file.seek(0)
        file.write(updated_content)
        file.truncate()

update_html_file(blog_index_path, new_entry_html, entry_date)
update_html_file(index_path, new_entry_html, entry_date)

print(f'Entradas actualizadas en blog.html e index.html')