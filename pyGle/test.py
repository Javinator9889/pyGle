#
#                py-google-search  Copyright (C) 2018  Javinator9889                
#   This program comes with ABSOLUTELY NO WARRANTY; for details add the "-h" option.
#           This is free software, and you are welcome to redistribute it
#                 under certain conditions; type "-L" for details.
#


def main():
    from bs4 import BeautifulSoup, Tag, ResultSet
    # import requests
    import lxml

    html = """<div class="g">
    <!--m-->
	<div data-hveid="53" data-ved="0ahUKEwivzbG55IzcAhXM6YMKHbwJA9sQFQg1KAEwAQ">
		<div class="rc">
			<h3 class="r">
				<a href="https://www.pinterest.es/pin/827395762766658506/" ping="/url?sa=t&amp;source=web&amp;rct=j&amp;url=https://www.pinterest.es/pin/827395762766658506/&amp;ved=0ahUKEwivzbG55IzcAhXM6YMKHbwJA9sQFgg2MAE">according to the chart and what we know, id say Meursault fits into the ...
				</a>
			</h3>
			<div class="s">
				<div>
					<div class="f hJND5c TbwUpd" style="white-space:nowrap">
						<cite class="iUh30">https://www.pinterest.es/pin/827395762766658506/</cite>
					</div>
					<span class="st">
						<span class="f">hace 15 horas - </span>Descubre ideas sobre <em>Psicologia</em> Forense .... <em>13</em> x 38 inches. ... icono de la literatura inglesa, no aprendió a hablar inglés hasta los <em>20</em> años. .... <em>15</em> things you didn't know about the dead. .... <em>10</em> Reasons Why Men And Women Are Different #<wbr>boysvsgirls ... Psychopath <em>test</em>..everyone should take it...while I scored 4/<em>11</em> I was<wbr> ...</wbr></wbr>
					</span>
				</div>
			</div>
		</div>
	</div>
	<!--n-->
</div>"""
    soup = BeautifulSoup(html, "lxml")
    class_g: ResultSet = soup.find_all("div", {"class": "g"})
    for a in class_g:
        rc: ResultSet = a.find_all("h3", {"class": "r"})
        # print(rc)
        for b in rc:
            a1: ResultSet = b.find_all("a")
            # print(a1)
            for c in a1:
                print("Link: " + c.get("href"))
                print("Website name: " + c.string)
            s: ResultSet = a.find_all("div", {"class": "s"})
            # print(s)
            for d in s:
                st: ResultSet = d.find_all("span", {"class": "st"})
                # print(st)
                for e in st:
                    # print(e)
                    f: ResultSet = e.find_all("span", {"class": "f"})
                    # print(f)
                    for f1 in f:
                        print("Date: " + f1.string)
                        print("Description: " + e.text.replace(f1.string, ''))

    
if __name__ == '__main__':
    main()
