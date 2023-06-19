import json
import os
import threading
import time
from time import sleep

import flet as ft

from Archive import EXPORT_FILE, Archive
from Functions import estimate_time, LOADING_REFERSH_TIME


class GUI:
    def __init__(self):
        self.tickets = []
        self.loading_bar_reviewers = []
        self.loading_bar_cinemas = []
        self.retrieve_button = None
        self.buttons = []
        self.screening_enable_button = None
        self.archive = None
        self.search_button = None

    def initialize(self):
        def main(page: ft.Page):
            page.title = "Cinema Crawler"
            page.scroll = "always"
            page.window_height = 600
            page.window_width = 480
            page.vertical_alignment = ft.MainAxisAlignment.CENTER

            def loading_bar_initial():
                self.start_time = time.time()
                self.loading_bar_cinemas.append(ft.ProgressBar(width=400))
                self.loading_bar_cinemas.append(ft.Text("Retrieving movies", style="headlineSmall", color="blue"))
                self.loading_bar_cinemas.append(
                    ft.Column([ft.Text("This may take a short while."), self.loading_bar_cinemas[0]]))
                page.add(self.loading_bar_cinemas[1], self.loading_bar_cinemas[2],
                         )

                # progress = {'progress': 0}
                # while progress['progress'] < 100:
                #     progress = self.archive.get_movie_screenings_progress()
                #     self.loading_bar_cinemas[0].value = progress['progress'] * 0.01
                #     sleep(LOADING_REFERSH_TIME)
                #     estimate_timed = estimate_time(
                #         start_time=self.start_time, current_item=progress['current'] + 1,
                #         total_items=progress['total'])
                #
                #     page.remove(self.loading_bar_cinemas[2])
                #     self.loading_bar_cinemas[2] = ft.Column([ft.Text(estimate_timed), self.loading_bar_cinemas[0]])
                #     page.add(self.loading_bar_cinemas[2])
                #     page.update()

            def loading_bar_subsequent():
                page.remove(self.loading_bar_cinemas[1], self.loading_bar_cinemas[2], )
                self.loading_bar_cinemas.clear()
                page.update()
                # -------------------

                self.start_time = time.time()
                self.loading_bar_reviewers.append(ft.ProgressBar(width=400))
                self.loading_bar_reviewers.append(ft.Text("Collecting ratings", style="headlineSmall", color="amber"))
                self.loading_bar_reviewers.append(ft.Column([ft.Text("Just a moment!"), self.loading_bar_reviewers[0]]))
                page.add(self.loading_bar_reviewers[1], self.loading_bar_reviewers[2],
                         )

                progress = {'progress': 0}
                while progress['progress'] < 100:
                    progress = self.archive.get_reviewers_progress()
                    self.loading_bar_reviewers[0].value = progress['progress'] * 0.01
                    sleep(LOADING_REFERSH_TIME)
                    estimate_timed = estimate_time(
                        start_time=self.start_time, current_item=progress['current'] + 1,
                        total_items=progress['total'])

                    page.remove(self.loading_bar_reviewers[2])
                    self.loading_bar_reviewers[2] = ft.Column([ft.Text(estimate_timed), self.loading_bar_reviewers[0]])
                    page.add(self.loading_bar_reviewers[2])
                    page.update()

                page.remove(self.loading_bar_reviewers[1], self.loading_bar_reviewers[2], )
                self.loading_bar_reviewers.clear()
                page.update()

            txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

            def start(e):
                # e.control.disabled = True
                def get_json():
                    print("Starting.")

                    self.start_time = time.time()

                    self.archive = Archive(
                        checklist=get_checked_items(),
                        is_screenings=self.screening_enable_button.value, custom_search=custom_search())
                    remove_json()
                    thread_1 = threading.Thread(target=loading_bar_initial)
                    thread_1.start()
                    self.archive.initialize_cinemas()
                    thread_1.join()
                    thread_2 = threading.Thread(target=loading_bar_subsequent)
                    thread_2.start()
                    self.archive.initialize_reviewers()
                    thread_2.join()
                    page.remove(self.retrieve_button)
                    add_json()

                get_json()

            def remove_json():
                for ticket in self.tickets:
                    page.remove(ticket)
                self.tickets.clear()
                page.update()

            def generate_screenings(screenings):

                def generate_hours(hours):
                    tickets = []
                    for hour in hours:
                        tickets.append(ft.TextButton(hour,

                                                     ))

                    all = []
                    divide = []

                    for x in range(len(tickets)):
                        divide.append(tickets[x])
                        if x == len(tickets) - 1:
                            all.append(ft.Row(divide))
                            divide = []
                        elif x % 5 == 4:
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

            def get_checked_items():
                return [button.tooltip.replace(' ', '') for button in self.buttons if button.value]

            def custom_search():
                return self.search_button.value
            def custom_search_change(e):
                for button in self.buttons[:3]:
                    button.value = False
                    if not e.control.value:
                        button.disabled = False
                    else:
                        button.disabled = True
                page.update()

            def generate_top_buttons():
                l = [ft.IconButton(
                    icon=ft.icons.PLAY_CIRCLE_OUTLINE_SHARP,
                    icon_color="blue400",
                    icon_size=50,
                    tooltip="Find nearby movies!",
                    on_click=start,
                    data=None,

                )]
                self.screening_enable_button = ft.Switch(value=True)
                self.search_button = ft.TextField(on_change=custom_search_change, label="Custom Search", width=150, on_submit=custom_search)
                l.append(ft.Row([self.search_button, self.screening_enable_button,
                                    ft.Text("Get screenings?", style="titleSmall")]))
                self.buttons.append(ft.Checkbox(data='Z70MR', label='  ', value=False, tooltip="Yes Planet"))
                self.buttons.append(ft.Checkbox(data='Z7RJ0', label='  ', value=False, tooltip="Cinema City"))
                self.buttons.append(ft.Checkbox(data='Z7qum', label='  ', value=False, tooltip="Hot Cinema"))
                self.buttons.append(ft.Checkbox(data='Z7UUU', label='  ', value=False, tooltip="IMDB"))
                self.buttons.append(ft.Checkbox(data='Z7kQB', label='  ', value=False, tooltip="Metacritic"))
                self.buttons.append(ft.Checkbox(data='Z7neQ', label='  ', value=False, tooltip="RottenTomatoes"))

                avatars = [ft.CircleAvatar(tooltip=button.tooltip, foreground_image_url='https://imgtr.ee/images/2023/06/18/{id}.png'
                                           .format(id=button.data))  for button in self.buttons]

                page.add(ft.Container(content=ft.Column([ft.Row(l),
                                                         ft.Row(avatars),
                                                         ft.Row(self.buttons)
                                                         ])))

            def copy_clipboard(e):
                page.set_clipboard(e.control.data)

            def collapse_text(e, hidden, empty):
                if hasattr(e.control.subtitle, 'value'):
                    if e.control.subtitle.value == empty.value:
                        return
                    elif e.control.subtitle.value == hidden.value:
                        e.control.subtitle = e.control.data
                else:
                    e.control.subtitle = hidden

                page.update()

            def add_json():
                page.add(
                    self.retrieve_button
                )
                data = read_json()
                icons = {'genre': ft.icons.ALBUM,
                         'duration': ft.icons.TIMER,
                         'trailer': ft.icons.VIDEO_LIBRARY_ROUNDED}

                for movie in data:
                    attributes = [ft.ListTile(
                        leading=ft.Icon(icons[key]),
                        title=ft.Text(
                            key.capitalize()),
                        subtitle=ft.Text(movie[key]),
                    ) for key in movie if key in ['genre'] and movie[key]] \
                                 + \
                                 [ft.ListTile(
                                     leading=ft.Icon(icons[key]),
                                     title=ft.Text(
                                         key.capitalize()),
                                     subtitle=ft.Text(movie[key][:60] + '...'),
                                     data=movie[key], on_click=copy_clipboard,
                                 ) for key in movie if key in ['trailer'] and movie[key]]

                    screenings_data = {'hidden': ft.Text('Click to show screenings.', color="blue400"),
                                       'shown': ft.Container(content=ft.Column(
                                           generate_screenings(movie['screenings']))),
                                       'empty': ft.Text('None for today.', color="pink600")}

                    screenings = [
                        ft.ListTile(on_click=lambda e: collapse_text(e, screenings_data['hidden'], screenings_data['empty']),
                                    data=screenings_data['shown'],
                                    title=ft.Text(
                                        'Screenings'),
                                    subtitle=screenings_data['hidden'] if movie['screenings'] else screenings_data['empty'],
                                    ),
                    ] if self.screening_enable_button.value else []
                    attributes = [
                                     ft.ListTile(
                                         leading=ft.Icon(ft.icons.STAR),
                                         title=ft.Text(
                                             str(movie['total_rating'])[:4], style="titleLarge"),
                                         subtitle=ft.Text('• ' +
                                                          '\n• '.join(
                                                              [str(key) + ': ' + str(movie['rating'][key]) for key in
                                                               movie['rating']])
                                                          ),
                                     )] + attributes + screenings

                    for attribute in attributes:
                        key = attribute.title.value.lower()
                        if key.isdigit():  # Removes rating if it didn't extract it.
                            if float(key) == 0:
                                attributes.remove(attribute)

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
                                            subtitle=ft.Text(movie['duration'],
                                                             ),
                                        ),
                                    ]),
                                    ft.Column(attributes),
                                    ft.Row(
                                        [ft.TextButton("Show details"),],
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
