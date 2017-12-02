import xlsxwriter

workbook = xlsxwriter.Workbook('stats.xlsx')
worksheet = workbook.add_worksheet()

def main():
    size = None
    for x in xrange(1, 3):
        f = open('data' + str(x) + '.out')
        data = f.read()
        size = len(data.split('\n')) - 1
        f.close()
        line_no = 1
        for line in data.split('\n'):
            if line == '':
                break
            t = int(float(line.split(' ')[1]) * 1000000)
            worksheet.write(chr(ord('A') + x - 1) + str(line_no), t)
            worksheet.write('D' + str(line_no), len(line.split(' ')[0]))
            #worksheet.write('E' + str(line_no), line.split(' ')[2])
            #worksheet.write('F' + str(line_no), line.split(' ')[3])
            line_no += 1

    chart = workbook.add_chart({'type': 'line'})
    chart.set_x_axis({
            'name': 'Input #',
            'name_font': {'size': 14, 'bold': True},
        })
    chart.set_y_axis({
        'name': 'Time(nanoseconds)',
        'name_font': {'size': 14, 'bold': True},
    })
    chart.add_series({'name': 'normal',     'values': '=Sheet1!$A$1:$A$%s' % str(size)})
    chart.add_series({'name': 'pollard', 'values': '=Sheet1!$B$1:$B$%s' % str(size)})
    worksheet.insert_chart('G8', chart)

    chart = workbook.add_chart({'type': 'column'})
    chart.set_x_axis({
            'name': 'Input #',
            'name_font': {'size': 14, 'bold': True},
        })
    chart.set_y_axis({
        'name': 'Digits',
        'name_font': {'size': 14, 'bold': True},
    })
    chart.add_series({'values': '=Sheet1!$D$1:$D$%s' % str(size)})
    worksheet.insert_chart('G23', chart)
    workbook.close()

if __name__ == '__main__':
    main()