import os
from datetime import datetime

# Configuración
blog_dir = os.path.join(os.path.dirname(__file__), 'blog')
index_path = os.path.join(os.path.dirname(__file__), 'index.html')

def get_blog_entries(blog_dir):
    entries = []
    for filename in os.listdir(blog_dir):
        if filename.endswith('.html'):
            filepath = os.path.join(blog_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                title_start = content.find('<h2>') + 4
                title_end = content.find('</h2>', title_start)
                title = content[title_start:title_end]

                date_start = content.find('Fecha: ') + 7
                date_end = content.find('</span>', date_start)
                date_str = content[date_start:date_end]

                try:
                    date = datetime.strptime(date_str, "%d/%m/%Y")
                except ValueError:
                    print(f"Fecha no válida en {filename}: {date_str}")
                    continue

                image_start = content.find('<img src="') + 10
                image_end = content.find('"', image_start)
                image = content[image_start:image_end]

                entries.append({
                    'title': title,
                    'date': date,
                    'image': image,
                    'filename': filename
                })
    return sorted(entries, key=lambda x: x['date'], reverse=True)

def update_index_html(index_path, recent_entries):
    with open(index_path, 'r+', encoding='utf-8') as file:
        content = file.read()
        start_pos = content.find('<div class="blog-entries">')
        end_pos = content.find('</div>', start_pos) + len('</div>')
        entries_content = content[start_pos:end_pos]

        new_entries_html = '<div class="blog-entries">'
        for entry in recent_entries[:3]:
            new_entries_html += f'''
            <article class="blog-entry">
                <img src="{entry['image']}" alt="Imagen de la {entry['title']}">
                <div class="entry-content">
                    <h3><a href="blog/{entry['filename']}">{entry['title']}</a></h3>
                    <span class="entry-date">Fecha: {entry['date'].strftime("%d/%m/%Y")}</span>
                </div>
            </article>
            '''
        new_entries_html += '</div>'

        updated_content = content[:start_pos] + new_entries_html + content[end_pos:]
        file.seek(0)
        file.write(updated_content)
        file.truncate()

# Obtener las entradas del blog
blog_entries = get_blog_entries(blog_dir)

# Actualizar index.html con las 3 entradas más recientes
update_index_html(index_path, blog_entries)

print(f'index.html actualizado con las 3 entradas más recientes')