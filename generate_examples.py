import os
from glob import glob
import random
import itertools


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
methods = ['ours', 'stargan2', 'sam', 'styleclip']
method_names = ['Ours', 'StarGAN v2', 'SAM', 'StyleCLIP']
image_ext = 'jpg'

###

originals = glob(f'{original_folder}/*.{image_ext}')
originals = [os.path.splitext(os.path.basename(o))[0] for o in originals]
random.shuffle(originals)  ## e.g. "input_1880_0"
if N is None: N = len(originals)


html_out = open(output_file, 'w')

## Header

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
""", file=html_out)
print(f"""
        <p>Below, we visualize {N}{" random" if N < len(originals) else ""} examples of faces from our Faces Through Time validation set and their transformations to decades from 1880 to 2010 using our method. We highlight our method's inversions with red boxes.</p>
        {f'<p>You may also view a larger visualization (of {len(originals)} examples from our validation set) <a href="./examples_full.html">here</a> — <b>clicking this link loads 2 GB of data!</b> Recommonded: open this link in incognito mode to prevent browser caching and slowness.</p>' if N < len(originals) else ""}
""", file=html_out)

## Filters

print(f"""
        Filter by year:
        <select id="years_filter">
            <option value="source-all">All</option>
            {''.join(f'<option value="source-{y}">{y}</option>' for y in range(1880, 2020, 10))}
        </select>
""", file=html_out)

print(f"""
        &emsp;&emsp;
        Filter by method:
        <select id="methods_filter">
            {''.join(f'<option value="method-{m}">{mn}</option>' for m, mn in zip(methods, method_names))}
        </select>

""", file=html_out)

print(f"""
        <hr>
""", file=html_out)

## Data

for original_file in originals[:N]:
    source_year = int(original_file.split('_')[1])
    print(f"""
            <div class="source-all source-{source_year}">
                <table>
                    <tr style="empty-cells: show;">
                        <td class="year-label">Input ({source_year})</td>
                        <td>&nbsp;&nbsp;</td>
                        {''.join(f'<td class="year-label">{y}</td>' for y in range(1880, 2020, 10))}
                    </tr>
                    {''.join(
                        f'<tr class="method-all method-{method}"' + (' style="display: none;"' if method != methods[0] else '') + '>'
                        + f'<td><img src="{original_folder}/{original_file}.{image_ext}"></td><td></td>'
                        + ''.join(
                            f'<td><img src="{results_folder}/{method}/{original_file}_target_{target_year}.{image_ext}"'
                            + (' class="selected"' if source_year == target_year else '')
                            + "></td>"
                        for target_year in range(1880, 2020, 10) )
                        + '</tr>'
                    for method in methods )}
                </table>
                <hr>
            </div>
    """, file=html_out)

## Javascript

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

            const methods_filter = document.getElementById('methods_filter');
            $("#methods_filter").change(function() {
                $(".method-all").css("display", "none");
                $("." + methods_filter.value).css("display", "");
            })
        </script>
    </body>
</html>
""", file=html_out)

html_out.close()
