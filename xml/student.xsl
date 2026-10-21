<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:output method="html" indent="yes"/>

    <xsl:template match="/">
        <html>
        <head>
            <title>Student Details</title>

            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 30px;
                    background-color: #f5f9ff;
                }

                h2 {
                    text-align: center;
                    color: #003366;
                }

                table {
                    border-collapse: collapse;
                    width: 80%;
                    margin: 20px auto 40px auto;
                    background-color: white;
                }

                th, td {
                    border: 2px solid #333333;
                    padding: 12px;
                    text-align: center;
                }

                th {
                    background-color: lightblue;
                    color: black;
                }

                tr:nth-child(even) {
                    background-color: #eaf4ff;
                }
            </style>
        </head>

        <body>
            <h2>All Student Details (Sorted by Year)</h2>

            <table>
                <tr>
                    <th>Name</th>
                    <th>Department</th>
                    <th>Year</th>
                    <th>Mark</th>
                </tr>

                <xsl:for-each select="/students/student">
                    <xsl:sort select="year"
                        data-type="number" order="descending"/>
                    <xsl:sort select="name"
                        data-type="text" order="ascending"/>

                    <tr>
                        <td><xsl:value-of select="name"/></td>
                        <td><xsl:value-of select="department"/></td>
                        <td><xsl:value-of select="year"/></td>
                        <td><xsl:value-of select="mark"/></td>
                    </tr>
                </xsl:for-each>
            </table>

            <h2>IT Department Students (XPath Filter)</h2>

            <table>
                <tr>
                    <th>Name</th>
                    <th>Department</th>
                    <th>Year</th>
                    <th>Mark</th>
                </tr>

                <xsl:for-each select="/students/student[department='IT']">
                    <xsl:sort select="name"
                        data-type="text" order="ascending"/>

                    <tr>
                        <td><xsl:value-of select="name"/></td>
                        <td><xsl:value-of select="department"/></td>
                        <td><xsl:value-of select="year"/></td>
                        <td><xsl:value-of select="mark"/></td>
                    </tr>
                </xsl:for-each>
            </table>
        </body>
        </html>
    </xsl:template>

</xsl:stylesheet>
