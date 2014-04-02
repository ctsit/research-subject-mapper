<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0" xmlns:date="http://exslt.org/dates-and-times"
                extension-element-prefixes="date">
                <xsl:import href="date.date.template.xsl" />
                
    <xsl:output method="xml" version="4.0" encoding="UTF-8" indent="yes" />
    <!-- Creating a key for subject ID -->
    <xsl:key name="itemBySubID" match="item" use="dm_subjid"/>
    
    <!-- Copy everything from the source -->
    <xsl:template match=" node()|@*">
         <xsl:copy>
               <xsl:apply-templates select="node()|@*" />
         </xsl:copy>
     </xsl:template>
     <!-- Remove items with null start date -->
     <xsl:template match="item[descendant::dm_rfstdtc[. = '']]"/>
     <!-- Select only one subject -->
     <xsl:template match=
  "item[not(generate-id() = generate-id(key('itemBySubID', dm_subjid)[1]))]"
  />
        <!-- Drop the redcap_event_name  -->
     <xsl:template match="redcap_event_name"/>
     
        <!-- copy subject id and add new siteid -->
     <xsl:template match="dm_subjid">
        <research_subject_id>
            <xsl:value-of select="." />
        </research_subject_id>
        <site_id>
            <xsl:value-of select="substring-before(.,'-')" />
        </site_id>
    </xsl:template>
    
    
        <!-- copy start dates -->
     <xsl:template match="dm_rfstdtc">
       <start_date>
        <xsl:value-of select="." />
       </start_date>
    </xsl:template>
    
    <!-- set enddate to sysdate if enddate is not set -->
    <xsl:variable name="dateNow" select="date:date()"/>
    <xsl:template match="eot_dsstdtc[. = '']">
        <end_date>
            <xsl:value-of select="substring-before($dateNow,'-04:00')" />
        </end_date>
    </xsl:template>
    <!-- copy enddate if it is already set -->
    <xsl:template match="eot_dsstdtc">
       <end_date>
        <xsl:value-of select="." />
       </end_date>
    </xsl:template>
    


    <!-- remove all elements which have no value -->
    <xsl:template match=
    "*[not(@*|*|comment()|processing-instruction()) 
     and normalize-space()='']"/>

       

</xsl:stylesheet>