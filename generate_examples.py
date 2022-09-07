import os
from glob import glob
import random


output_file = 'examples.html'
N = 100
#
# output_file = 'examples_full.html'
# N = None


## Assuming a file structure like:
# assets/originals/input_1880_0.jpg
# assets/results/input_1880_0_target_2000.jpg

original_folder = 'assets/originals'
results_folder = 'assets/results'
image_ext = 'jpg'

###

originals = glob(f'{original_folder}/*.{image_ext}')
originals = [os.path.splitext(os.path.basename(o))[0] for o in originals]
random.shuffle(originals)  ## e.g. "input_1880_0"
if N is None: N = len(originals)

with open(output_file, 'w') as html_out:
    print("""
    <!doctype html>
    <html lang="en">

        <head>
            <meta charset="utf-8">
            <title>Examples — Faces Across Time</title>
            <style>
                img {
                    width: 95%;
                }
                .year-label {
                    font-weight: bold;
                    text-align: center;
                }
                img {
                    border: 4px solid;
                    border-color: white;
                }
                .selected {
                    border-color: red;
                }
            </style>
            <script src="https://code.jquery.com/jquery-3.3.1.min.js" type="text/javascript"></script>
        </head>

        <body>
            <h1>Dataset Examples ― "Transforming Faces Across Time"</h1>
    """,
    file=html_out)

    if N < len(originals):
        more_examples_str = f"<p>You may also view a larger visualization (of {len(originals)} examples from our validation set — <b>500 MB</b>) <a href=\"./examples_full.html\">here</a>. Recommonded: open this link in incognito mode to prevent browser caching and slowness.</p>"
    else:
        more_examples_str = ""

    print(f"""
            <p>Below, we visualize {N} examples of faces from our Faces Through Time validation set and their transformations to decades from 1880 to 1990 using our method. We highlight our method's inversions with red boxes.</p>
            {more_examples_str}
            Filter by year:
            <select id="years_filter">
                <option value="source-all">All</option>
                <option value="source-1880">1880</option>
                <option value="source-1890">1890</option>
                <option value="source-1900">1900</option>
                <option value="source-1910">1910</option>
                <option value="source-1920">1920</option>
                <option value="source-1930">1930</option>
                <option value="source-1940">1940</option>
                <option value="source-1950">1950</option>
                <option value="source-1960">1960</option>
                <option value="source-1970">1970</option>
                <option value="source-1980">1980</option>
                <option value="source-1990">1990</option>
                <option value="source-2000">2000</option>
                <option value="source-2010">2010</option>
            </select>
            <hr>
    """,
    file=html_out)
    ###
    for i, original_file in enumerate(originals):
        if i == N: break
        ## assuming original_file like: input_1880_0
        source_year = int(original_file.split('_')[1])
        print(f"""
                <div class="source-all source-{source_year}">
                    <table>
                        <tr style="empty-cells: show;">
                            <td class="year-label">Input ({source_year})</td>
                            <td>&nbsp;&nbsp;</td>
                            <td class="year-label">1880</td>
                            <td class="year-label">1890</td>
                            <td class="year-label">1900</td>
                            <td class="year-label">1910</td>
                            <td class="year-label">1920</td>
                            <td class="year-label">1930</td>
                            <td class="year-label">1940</td>
                            <td class="year-label">1950</td>
                            <td class="year-label">1960</td>
                            <td class="year-label">1970</td>
                            <td class="year-label">1980</td>
                            <td class="year-label">1990</td>
                        </tr>
                        <tr>
                            <td><img src="{original_folder}/{original_file}.{image_ext}"></td>
                            <td></td>
            """,
            file=html_out)
        for target_year in range(1880, 2000, 10):
            selected = "class=\"selected\"" if source_year == target_year else ""
            print(f"""
                                <td><img src="{results_folder}/{original_file}_target_{target_year}.{image_ext}" {selected}></td>
                """,
                file=html_out)
        print("""
                        </tr>
                    </table>
                    <hr>
                </div>
        """,
        file=html_out)
    print("""
            <script>
                const years_filter = document.getElementById('years_filter');
                $("#years_filter").change(function() {
                    if(years_filter.value == 'source-all') {
                        $(".source-all").css("display", "block");
                    } else {
                        $(".source-all").css("display", "none");
                        $("." + years_filter.value).css("display", "block");
                    }
                })
            </script>
        </body>
    </html>
    """,
    file=html_out)
