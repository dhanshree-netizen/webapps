<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:output method="html" indent="yes" encoding="UTF-8"/>

    <xsl:template match="/">
        <html>
            <head>
                <title>Student Details</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 30px;
                    }

                    h2 {
                        text-align: center;
                    }

                    table {
                        border-collapse: collapse;
                        width: 70%;
                        margin: auto;
                    }

                    th, td {
                        border: 1px solid black;
                        padding: 10px;
                        text-align: center;
                    }

                    th {
                        background-color: lightblue;
                    }
                </style>
            </head>

            <body>
                <h2>Student Details</h2>

                <table>
                    <tr>
                        <th>Name</th>
                        <th>Department</th>
                        <th>Year</th>
                    </tr>

                    <xsl:for-each select="students/student">
                        <tr>
                            <td>
                                <xsl:value-of select="name"/>
                            </td>

                            <td>
                                <xsl:value-of select="department"/>
                            </td>

                            <td>
                                <xsl:value-of select="year"/>
                            </td>
                        </tr>
                    </xsl:for-each>
                </table>
            </body>
        </html>
    </xsl:template>

</xsl:stylesheet>