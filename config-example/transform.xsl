<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0" xmlns:date="http://exslt.org/dates-and-times"
                extension-element-prefixes="date">
                <xsl:import href="date.date.template.xsl" />
                
    <xsl:output method="xml" version="4.0" encoding="UTF-8" indent="yes" />
    <!-- <xsl:template match="/records">
        <xsl:value-of select="/records"/>
    </xsl:template> -->


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
       <!-- <xsl:value-of select="substring-before(.,'-')" /> -->
    </xsl:template>
    <!-- <xsl:template match="site_id[. = '']">
        <site_id>100</site_id>
    </xsl:template> -->
     <xsl:template match="dm_rfstdtc">
	   <start_date>
        <xsl:apply-templates select="@* | node()" />
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
        <xsl:apply-templates select="@* | node()" />
	   </enddate>
	</xsl:template>
    

     <xsl:template match=
    "*[not(@*|*|comment()|processing-instruction()) 
     and normalize-space()=''
      ]"/>

       

</xsl:stylesheet>