function createTable(tableElement, data) {
    var rowTitles = data["rowTitles"];
    var colTitles1 = data["colTitles1"];
    var colTitles2 = data["colTitles2"];
    var tableData = data["tableData"];

    var tr;
    var td;

    // first row
    tr = document.createElement("tr");
    tableElement.appendChild(tr);
    for (var iCol = 0; iCol < colTitles1.length + 1; iCol++) {
        if (iCol === 0) {
            td = document.createElement("td");
            tr.appendChild(td);
            td.setAttribute("rowspan", "2");
        } else {
            td = document.createElement("td");
            tr.appendChild(td);
            td.setAttribute("colspan", colTitles2.length);
            td.innerHTML = colTitles1[iCol - 1];
        }
    }

    // second row
    tr = document.createElement("tr");
    tableElement.appendChild(tr);
    for (var iCol1 = 0; iCol1 < colTitles1.length; iCol1++) {
        for (var iCol2 = 0; iCol2 < colTitles2.length; iCol2++) {
            td = document.createElement("td");
            tr.appendChild(td);
            td.innerHTML = colTitles2[iCol2];
        }
    }

    // other rows
    for (var iRow = 0; iRow < rowTitles.length; iRow++) {
        tr = document.createElement("tr");
        tableElement.appendChild(tr);
        td = document.createElement("td");
        tr.appendChild(td);
        td.innerHTML = rowTitles[iRow];
        for (var jCol1 = 0; jCol1 < colTitles1.length; jCol1++) {
            for (var jCol2 = 0; jCol2 < colTitles2.length; jCol2++) {
                td = document.createElement("td");
                tr.appendChild(td);
                td.innerHTML = tableData[colTitles1[jCol1]][colTitles2[jCol2]][rowTitles[iRow]];
            }
        }
    }
}

var tableToExcel = (function () {
        var uri = 'data:application/vnd.ms-excel;base64,',
            template = '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet><x:Name>{worksheet}</x:Name><x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]--></head><body><table>{table}</table></body></html>',
            base64 = function (s) {
                return window.btoa(unescape(encodeURIComponent(s)))
            },
            format = function (s, c) {
                return s.replace(/{(\w+)}/g,
                    function (m, p) {
                        return c[p];
                    })
            }
        return function (tableObj, name) {
            var ctx = {worksheet: name || 'sheet1', table: tableObj.innerHTML};
            window.location.href = uri + base64(format(template, ctx));
        }
    })()

