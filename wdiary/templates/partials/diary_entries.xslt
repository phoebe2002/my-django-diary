<!-- diary_entries.xslt -->

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="/">
    <html>
      <head>
        <style>
          /* Add your styling here */
          body {
            font-family: Arial, sans-serif;
            margin: 20px;
          }
          h2 {
            color: #800080;
          }
          /* Add more styling rules as needed */
        </style>
      </head>
      <body>
        <h2>Diary Entries</h2>
        <xsl:apply-templates select="/diary_entries/entry"/>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="entry">
    <div>
      <h3><xsl:value-of select="title"/></h3>
      <p><xsl:value-of select="content"/></p>
      <p>Date: <xsl:value-of select="date"/></p>
      <hr/>
    </div>
  </xsl:template>
</xsl:stylesheet>
