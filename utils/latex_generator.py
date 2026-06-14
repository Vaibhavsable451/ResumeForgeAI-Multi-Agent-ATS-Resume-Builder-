def generate_latex(
        resume):

    latex = f"""
\\documentclass{{article}}

\\usepackage[a4paper,margin=1in]{{geometry}}

\\begin{{document}}

{resume}

\\end{{document}}
"""

    return latex