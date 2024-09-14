https://publicdomain-nocopyright.github.io/7DTD-Public-Vanilla-Server/7DTD_1_1_in_game_buttons_handlers/News.xml

#### Usage example
```
			    <rect pos="-45,45" width="164" height="32" depth="5" name="Button1" controller="NewsWindow" sources="https://publicdomain-nocopyright.github.io/7DTD-Public-Vanilla-Server/7DTD_1_1_in_game_buttons_handlers/News.xml">
					<sprite depth="0" name="backgroundFeatured" sprite="menu_empty" type="sliced" color="[darkGrey]" />
					<button depth="10" name="btnLink" style="hover,press" sprite="menu_empty" hoverscale="1" defaultcolor="0,0,0,1" hovercolor="100,100,100,100" type="sliced" />
					<label pos="0,0" style="header.name" height="32" width="164" justify="center" color="[white]" crispness="Never" effect="Outline8" effect_color="0,0,0,255" effect_distance="2,2" text="VanillaServer"/>
				</rect>
```

Note: 
```
<!--  sources="@modfolder:News.xml"     doesn't work, probably due to internal implementation to parse urls -->
```
