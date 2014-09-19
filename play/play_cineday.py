#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time
from droydrunner.uidevice import UiDevice

package_launcher = "com.sec.android.app.launcher"

package_cineday = "fr.orange.cineday"

d = UiDevice()

d.press('home')
d.press('home')



# click on cineday
cineday_selector  = d.device( packageName = package_launcher , text=u'Cinéday')
cineday_selector.click()


# splash screen
d.device.wait.update()



# main cineday page


# wait for  main tab (films/salles /mes codes/rechercher)
main_tab_selector = d.device( resourceId="android:id/tabs", packageName= package_cineday)
ok = main_tab_selector.wait(2000)


# click on films
films_selector = main_tab_selector.child(index= '0',className ="android.widget.RelativeLayout")
print films_selector
films_selector.click()


# click on salles
salles_selector = main_tab_selector.child(index= '1',className ="android.widget.RelativeLayout")
#salles_selector.click()


#click on rechercher
rechercher_selector = main_tab_selector.child(index= '3',className ="android.widget.RelativeLayout")
#rechercher_selector.click()



# click on films
#films_selector.click()


# selects films tabs
films_tabs_selector = d.device( resourceId="fr.orange.cineday:id/film_bottom")

sorties = d.device(resourceId = "fr.orange.cineday:id/btn_films_sorties")
affiche = d.device(resourceId = "fr.orange.cineday:id/btn_films_affiche")
bientot = d.device(resourceId = "fr.orange.cineday:id/btn_films_prochainement")


affiche.click()
bientot.click()


sorties.click()

d.device.wait.update()

# the list of film
film_list_view =  d.device(resourceId = "fr.orange.cineday:id/films_listview" ,scrollable = True)
ok = film_list_view.exists
#film_list_view.scroll(steps=10)

# select first film
first_film = film_list_view.child(resourceId="fr.orange.cineday:id/films_row" , index =0)
first_film.click()
d.device.wait.update()


# onefilm view
film_view = d.device( resourceId = 'fr.orange.cineday:id/film_details_principal_scroll_view')
film_view.scroll(steps=10)

d.device.screenshot('film.png')


d.device.press('back')



print
