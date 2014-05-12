<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
 <xsl:copy>
  <xsl:apply-templates select="@*|node()"/>
 </xsl:copy>
</xsl:template>
 <!-- copy start dates -->
     <xsl:template match="dm_brthyr">
       <yob>
        <xsl:value-of select="." />
       </yob>
    </xsl:template>
<xsl:template match="site_id" />
<xsl:template match="dm_subjid" />

</xsl:stylesheet>