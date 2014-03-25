<xsl:stylesheet version="1.0"
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
 <xsl:output omit-xml-declaration="yes" indent="yes"/>


 <xsl:key name="groups" match="item" use="site_id"/>

 <xsl:template match="/*">
  <sites>
   <xsl:apply-templates/>
  </sites>
 </xsl:template>

 <xsl:template match="item[generate-id()=generate-id(key('groups',site_id)[1])]">
  <site id="{site_id}">
   <xsl:copy-of select="key('groups',site_id)"/>
  </site>
 </xsl:template>
 
<xsl:template match="item[not(generate-id()=generate-id(key('groups',site_id)[1]))]"/>
</xsl:stylesheet>