<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
 <xsl:copy>
  <xsl:apply-templates select="@*|node()"/>
 </xsl:copy>
</xsl:template>
 
     <xsl:template match="study_subject_number">
       <tsn>
        <xsl:value-of select="." />
       </tsn>
    </xsl:template>
    <xsl:template match="study_subject_number_verifier_value">
       <yob>
        <xsl:value-of select="." />
       </yob>
    </xsl:template>

</xsl:stylesheet>