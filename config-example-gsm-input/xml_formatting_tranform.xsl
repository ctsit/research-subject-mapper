<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0" xmlns:date="http://exslt.org/dates-and-times"
                extension-element-prefixes="date">
                <xsl:import href="date.date.template.xsl" />
                
    <xsl:output method="xml" version="4.0" encoding="UTF-8" indent="yes" />
    <xsl:template match=" @* | node()">
         <xsl:copy>
               <xsl:apply-templates select="@* | node()" />
         </xsl:copy>
     </xsl:template>
     <xsl:template match="dm_subjid">
        <dm_subjid>
            <xsl:value-of select="." />
        </dm_subjid>
        <site_id>
            <xsl:value-of select="substring-before(.,'-')" />
        </site_id>
    </xsl:template>
    
     <xsl:template match="dm_rfstdtc">
	   <start_date>
        <xsl:value-of select="." />
	   </start_date>
	</xsl:template>
    
    <xsl:variable name="dateNow" select="date:date()"/>
    <xsl:template match="eot_dsstdtc[. = '']">
        <enddate>
            <xsl:value-of select="substring-before($dateNow,'-04:00')" />
        </enddate>
    </xsl:template>
	<xsl:template match="eot_dsstdtc">
	   <enddate>
        <xsl:value-of select="." />
	   </enddate>
	</xsl:template>
    

    <xsl:template match=
    "*[not(@*|*|comment()|processing-instruction()) 
     and normalize-space()='']"/>

       

</xsl:stylesheet>