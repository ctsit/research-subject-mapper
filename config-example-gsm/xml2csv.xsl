<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="text" encoding="utf-8" />
       
  
  <xsl:param name="delim" select="','" />
  <xsl:param name="quote" select="'&quot;'" />
  <xsl:param name="break" select="'&#xA;'" />

  <xsl:template match="/">
    
    <xsl:if test="/records/item/mrn">
      <xsl:text>"research_subject_id,yob,end_date,start_date,mrn,facility_code" </xsl:text>
    </xsl:if>
    <xsl:if test="not(/records/item/mrn)">
      <xsl:text>"research_subject_id,person_index_yob,redcap_yob" </xsl:text></xsl:if>
    <xsl:value-of select="$break" />   
    <xsl:apply-templates select="records/item" />
  </xsl:template>

  <xsl:template match="item">
    <xsl:apply-templates />
    <xsl:if test="following-sibling::*">
      <xsl:value-of select="$break" />
    </xsl:if>
  </xsl:template>

  <xsl:template match="*">
    <xsl:value-of select="concat($quote, normalize-space(), $quote)" />
    <xsl:if test="following-sibling::*">
      <xsl:value-of select="$delim" />
    </xsl:if>
  </xsl:template>

  <xsl:template match="text()" />
</xsl:stylesheet>