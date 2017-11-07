import xlsxwriter

def main():
    data = [1, 2, 3]
    algorithm = 1
    workbook = xlsxwriter.Workbook('chart_linetest.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write_column('A1', data)
    chart = workbook.add_chart({'type': 'line'})
    chart.set_x_axis({
        'name': 'Number of digits',
        'name_font': {'size': 14, 'bold': True},
    })
    if algorithm == 1:
        chart.set_y_axis({
            'name': 'Time(milliseconds)',
            'name_font': {'size': 14, 'bold': True},
        })
    else:
        chart.set_x_axis({
            'name': 'Time(nanoseconds)',
            'name_font': {'size': 14, 'bold': True},
        })
    chart.add_series({'values': '=Sheet1!$A$1:$A$%s' % str(len(data) + 1)})
    worksheet.insert_chart('C1', chart)
    workbook.close()

main()