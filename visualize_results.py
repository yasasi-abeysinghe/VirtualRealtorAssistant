import json


def generate_output(json_results):
    # to open/create a new html file in the write mode
    f = open('output.html', 'w')

    # the html code which will go in the file GFG.html
    html_template = """<html>
    <head>
    <title>Virtual Realtor Assistant</title>
    </head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Karma">
    <style>
    body,h1,h2,h3,h4,h5,h6 {font-family: "Karma", sans-serif}
    .w3-bar-block .w3-bar-item {padding:20px}
    </style>
    </head>
    <body>
    
    <!-- Top menu -->
    <div class="w3-top">
      <div class="w3-white w3-xlarge" style="max-width:1200px;margin:auto">
        <div class="w3-center w3-padding-16">Virtual Realtor Assistant</div>
      </div>
    </div>
    
    <!-- !PAGE CONTENT! -->
    <div class="w3-main w3-content w3-padding" style="max-width:1200px;margin-top:100px">
    """

    count = 0
    for home in json_results[:8]:
        if count % 4 == 0:
            html_template += """
            <div class="w3-row-padding w3-padding-16 w3-center">
            """

        if home["photoUrls"] is None:
            html_template += """
                       <div class="w3-quarter">
                         <image style="width:200px;height:150px"
                         src="">
                         <h3>""" + str(home["streetLine"]) + """ """ + str(home["city"]) + """ """ + str(
                home["state"]) + """ """ + str(home["zip"]) + """</h3>
                         <h4>Price: """ + str(home["price"]) + """ , Beds = """ + str(
                home["beds"]) + """, Bath = """ + str(home["baths"]) + """, 
                         Sq Ft = """ + str(home["sqFt"]) + """</h4>
                         <p>More details: <a href=\"""" + str(home["url"]) + """\"> 
                         click here </a></p>
                       </div>
                       """

        else:
            html_template += """
            <div class="w3-quarter">
              <image style="width:200px;height:150px"
              src=\"""" + str(home["photoUrls"]) + """\">
              <h3>""" + str(home["streetLine"]) + """ """ + str(home["city"]) + """ """ + str(home["state"]) + """ """ + str(home["zip"]) + """</h3>
              <h4>Price: """ + str(home["price"]) + """ , Beds = """ + str(home["beds"]) + """, Bath = """ + str(home["baths"]) + """, 
              Sq Ft = """ + str(home["sqFt"]) + """</h4>
              <p>More details: <a href=\"""" + str(home["url"]) + """\"> 
              click here </a></p>
            </div>
            """
        count += 1
        if count % 4 == 0:
            html_template += """
            </div>"""

    html_template += """
    </div>
    
    </body>
    </html>
        """

    print(html_template)

    # writing the code into the file
    f.write(html_template)

    # close the file
    f.close()
