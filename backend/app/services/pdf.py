from weasyprint import HTML


def render_report(brand_name: str, rows: list[dict]) -> bytes:
    tr = ''.join([f"<tr><td>{r['candidate_name']}</td><td>{r['source']}</td><td>{r['score']}</td><td>{r['risk_level']}</td></tr>" for r in rows])
    html = f"""
    <html><body>
    <h1>DEPOZIO Brand Risk Report</h1>
    <h2>{brand_name}</h2>
    <table border='1' cellspacing='0' cellpadding='6'>
    <tr><th>Candidate</th><th>Source</th><th>Score</th><th>Risk</th></tr>{tr}
    </table></body></html>
    """
    return HTML(string=html).write_pdf()
