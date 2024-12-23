import os
from datetime import datetime

# Configuración
template_path = os.path.join(os.path.dirname(__file__), 'blog-entry-template.html')
output_dir = 'c:/Users/josed/Repositorios/PORTAFOLIO/'
blog_index_path = os.path.join(output_dir, 'blog.html')
index_path = os.path.join(output_dir, 'index.html')

entry_title = input("Introduce el título de la nueva entrada: ")
entry_date = datetime.now().strftime("%d/%m/%Y")
entry_filename = entry_title.lower().replace(' ', '-') + '.html'
entry_image = input("Introduce la ruta de la imagen de la entrada: ")

# Leer la plantilla
with open(template_path, 'r', encoding='utf-8') as file:
    template_content = file.read()

# Reemplazar el título, la fecha y la imagen en la plantilla
entry_content = template_content.replace('Título de la Entrada', entry_title)
entry_content = entry_content.replace('Fecha: DD/MM/YYYY', f'Fecha: {entry_date}')
entry_content = entry_content.replace('images/blog-image.jpg', entry_image)

# Guardar la nueva entrada
output_path = os.path.join(output_dir, entry_filename)
with open(output_path, 'w', encoding='utf-8') as file:
    file.write(entry_content)

print(f'Nueva entrada creada: {output_path}')

# Actualizar el archivo blog.html
new_entry_html = f'''
<article class="blog-entry">
    <img src="{entry_image}" alt="Imagen de la {entry_title}">
    <div class="entry-content">
        <h3><a href="{entry_filename}">{entry_title}</a></h3>
        <p>Resumen de la entrada...</p>
        <span class="entry-date">Fecha: {entry_date}</span>
    </div>
</article>
'''

with open(blog_index_path, 'r+', encoding='utf-8') as file:
    content = file.read()
    insert_pos = content.find('<div class="blog-entries">') + len('<div class="blog-entries">')
    updated_content = content[:insert_pos] + new_entry_html + content[insert_pos:]
    file.seek(0)
    file.write(updated_content)
    file.truncate()

# Actualizar el archivo index.html
with open(index_path, 'r+', encoding='utf-8') as file:
    content = file.read()
    insert_pos = content.find('<div class="blog-entries">') + len('<div class="blog-entries">')
    updated_content = content[:insert_pos] + new_entry_html + content[insert_pos:]
    file.seek(0)
    file.write(updated_content)
    file.truncate()

print(f'Entradas actualizadas en blog.html e index.html')