import os
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuración
blog_dir = os.path.join(os.path.dirname(__file__), 'blog')
index_path = os.path.join(os.path.dirname(__file__), 'index.html')
blog_index_path = os.path.join(os.path.dirname(__file__), 'blog.html')

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

def update_html_file(file_path, recent_entries):
    with open(file_path, 'r+', encoding='utf-8') as file:
        content = file.read()
        start_pos = content.find('<div class="blog-entries">')
        end_pos = content.find('</div>', start_pos) + len('</div>')

        existing_entries = content[start_pos:end_pos]
        new_entries_html = '<div class="blog-entries">'

        for entry in recent_entries[:3]:
            entry_html = f'''
            <article class="blog-entry">
                <img src="{entry['image']}" alt="Imagen de la {entry['title']}">
                <div class="entry-content">
                    <h3><a href="blog/{entry['filename']}">{entry['title']}</a></h3>
                    <span class="entry-date">Fecha: {entry['date'].strftime("%d/%m/%Y")}</span>
                </div>
            </article>
            '''
            if f'<a href="blog/{entry["filename"]}">' not in existing_entries:
                new_entries_html += entry_html
            else:
                # Actualizar la entrada existente
                existing_entry_start = existing_entries.find(f'<a href="blog/{entry["filename"]}">')
                existing_entry_end = existing_entries.find('</article>', existing_entry_start) + len('</article>')
                existing_entry_html = existing_entries[existing_entry_start:existing_entry_end]
                updated_entry_html = existing_entry_html.replace(
                    existing_entry_html[existing_entry_html.find('<img src="'):existing_entry_html.find('"', existing_entry_html.find('<img src="') + 10) + 1],
                    f'<img src="{entry["image"]}"'
                ).replace(
                    existing_entry_html[existing_entry_html.find('<h3><a href="'):existing_entry_html.find('</a>', existing_entry_html.find('<h3><a href="')) + 4],
                    f'<h3><a href="blog/{entry["filename"]}">{entry["title"]}</a>'
                )
                new_entries_html += updated_entry_html

        new_entries_html += '</div>'

        updated_content = content[:start_pos] + new_entries_html + content[end_pos:]
        file.seek(0)
        file.write(updated_content)
        file.truncate()

def update_entry_in_html(file_path, entry):
    with open(file_path, 'r+', encoding='utf-8') as file:
        content = file.read()
        entry_start = content.find(f'<a href="blog/{entry["filename"]}">')
        if entry_start != -1:
            title_start = content.find('>', entry_start) + 1
            title_end = content.find('</a>', title_start)
            image_start = content.rfind('<img src="', 0, entry_start) + 10
            image_end = content.find('"', image_start)

            updated_content = (
                content[:image_start] + f'<img src="{entry["image"]}"' + content[image_end:]
            )
            updated_content = (
                updated_content[:title_start] + entry['title'] + updated_content[title_end:]
            )

            file.seek(0)
            file.write(updated_content)
            file.truncate()

def update_entries():
    blog_entries = get_blog_entries(blog_dir)
    for entry in blog_entries:
        update_entry_in_html(index_path, entry)
        update_entry_in_html(blog_index_path, entry)
    update_html_file(index_path, blog_entries)
    update_html_file(blog_index_path, blog_entries)
    print(f'Entradas actualizadas en index.html y blog.html')

class BlogEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.html'):
            print(f'Archivo modificado: {event.src_path}')
            update_entries()

if __name__ == "__main__":
    event_handler = BlogEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path=blog_dir, recursive=False)
    observer.start()
    print(f'Monitoreando cambios en {blog_dir}...')

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("Monitoreo detenido.")
    observer.join()