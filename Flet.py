import json
import os
import threading
import time
from time import sleep

import flet as ft

from Archive import EXPORT_FILE, Archive
from Functions import estimate_time


class GUI():
    def __init__(self):
        self.tickets = []
        self.loading_bar = []
        self.retrieve_button = None
        self.archive = None

    def initialize(self):
        def main(page: ft.Page):
            page.title = "Cinema Crawler"
            page.scroll = "always"
            page.window_height = 600
            page.window_width = 480
            page.vertical_alignment = ft.MainAxisAlignment.CENTER

            def loading_bar():
                self.loading_bar.append(ft.ProgressBar(width=400))
                self.loading_bar.append(ft.Text("Retrieving movies", style="headlineSmall", color="amber"))
                self.loading_bar.append(ft.Column([ft.Text("Doing something..."), self.loading_bar[0]]))
                page.add(self.loading_bar[1], self.loading_bar[2],
                         )

                while (self.archive.get_progress() < 100):
                    self.loading_bar[0].value = self.archive.get_progress() * 0.01
                    sleep(1)
                    estimate_timed = estimate_time(
                        start_time=self.start_time, current_item=self.archive.current + 1,
                        total_items=self.archive.total)

                    page.remove(self.loading_bar[2])
                    self.loading_bar[2] = ft.Column([ft.Text(estimate_timed), self.loading_bar[0]])
                    page.add(self.loading_bar[2])
                    page.update()

                page.remove(self.loading_bar[1], self.loading_bar[2], )
                self.loading_bar.pop()
                self.loading_bar.pop()
                self.loading_bar.pop()
                page.update()

            txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

            def start(e):
                def get_json():
                    print("Starting.")

                    self.start_time = time.time()
                    self.archive = Archive(
                        checklist=['YesPlanet', 'RottenTomatoes', 'HotCinema', 'CinemaCity', 'IMDB', 'Metacritic'],
                        is_screenings=True)
                    threading.Thread(target=loading_bar).start()
                    remove_json()
                    page.remove(self.retrieve_button)
                    self.archive.initialize()
                    page.update()

                    add_json()

                get_json()

            def update_ticket_with_details(e):
                page.remove(self.tickets[-1])
                self.tickets.pop()
                page.update()


            def remove_json():
                while self.tickets:
                    page.remove(self.tickets[-1])
                    self.tickets.pop()
                    page.update()

            def generate_screenings(screenings):
                def generate_hours(hours):
                    tickets = []
                    for hour in hours:
                        tickets.append(ft.TextButton(
                        hour,
                        ))

                    all = []
                    divide = []

                    for x in range(len(tickets)):
                        divide.append(tickets[x])
                        if x%5==0:
                            all.append(ft.Row(divide))
                            divide = []

                    return all
                tickets = []
                for theatre in screenings:
                    screenings_buttons = generate_hours(screenings[theatre])
                    tickets.append(ft.ListTile(
                        leading=ft.Icon(ft.icons.LOCATION_PIN),
                        title=ft.Text(
                            theatre),
                        subtitle=ft.Container(content=ft.Column(
                                                screenings_buttons)
                        )
                    ))
                return tickets

            def generate_top_buttons():
                from PIL import Image
                items = ['YesPlanet', 'HotCinema', 'CinemaCity', 'RottenTomatoes', 'Metacritic', 'IMDB']
                l = [ft.IconButton(
                    icon=ft.icons.MOVIE_EDIT,
                    icon_color="blue400",
                    icon_size=40,
                    tooltip="Retrieve Movies",
                    on_click=start,
                    data=None,

                )]
                for item in items:
                    l.append(
                    ft.Image(
                        src="icons/{item}.png".format(item=item),
                        width=50,
                        height=50,
                        fit=ft.ImageFit.CONTAIN,
                    ))
                return l

            def add_json():
                page.add(
                    self.retrieve_button
                )
                data = read_json()
                for movie in data:
                    self.tickets.append(ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                [
                                    ft.Row([
                                        ft.Image(
                                        src=movie['image'],
                                        width=75,
                                        height=100,
                                        fit=ft.ImageFit.CONTAIN,
                                    ),
                                        ft.ListTile(

                                            title=ft.Text(
                                                movie['title']),
                                            subtitle=ft.Text(movie['origin']
                                                             ),
                                        ),
                                    ]),

                                    ft.ListTile(
                                        leading=ft.Icon(ft.icons.STAR),
                                        title=ft.Text(
                                            str(movie['total_rating'])[:4]),
                                        subtitle=ft.Text(
                                            movie['rating']
                                        ),
                                    ),

                                    ft.ListTile(
                                        leading=ft.Icon(ft.icons.ALBUM),
                                        title=ft.Text(
                                        'Genre'),
                                        subtitle=ft.Text(movie['genre']
                                        ),
                                    ),
                                    ft.ListTile(
                                        leading=ft.Icon(ft.icons.TIMER),
                                        title=ft.Text(
                                            'Duration'),
                                        subtitle=ft.Text(movie['duration']
                                                         ),
                                    ),
                                    ft.ListTile(
                                        leading=ft.Icon(ft.icons.MOVIE_FILTER),
                                        title=ft.Text(
                                            'Trailer'),
                                        subtitle=ft.Text(movie['trailer']
                                                         ),
                                    ),
                                    ft.ListTile(
                                        title=ft.Text(
                                            'Screenings'),
                                        subtitle=ft.Container(content=ft.Column(
                                                generate_screenings(movie['screenings']))),
                                    ),
                                    ft.Row(
                                        [ft.TextButton("Show details", on_click=update_ticket_with_details),
                                         ft.TextButton("Listen"),
                                         ],
                                        alignment=ft.MainAxisAlignment.END,
                                    ),
                                    ]
                            ),
                            width=430,
                            padding=10,
                        )
                    ))
                    page.add(self.tickets[-1]
                             )
                page.update()

            self.retrieve_button = ft.Row(controls=generate_top_buttons())

            add_json()

        ft.app(target=main)


def read_json():
    if not os.path.exists(EXPORT_FILE):
        with open(EXPORT_FILE, 'w') as f:
            f.write('[]')
    f = open(EXPORT_FILE, 'r')
    try:
        json_data = json.loads(f.read())
    except:
        json_data = {}
    f.close()
    return json_data


gui = GUI()
gui.initialize()
