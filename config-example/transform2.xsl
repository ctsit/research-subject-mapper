<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:key name="items-by-siteid" match="item" use="site_id" />
   <xsl:template match="records">
    
      <xsl:for-each select="item[generate-id(.) = generate-id(key('items-by-siteid', site_id)[1])]">
        <sites>
        <site>
          
              <xsl:call-template name="temp"/>
          
       
        </site>
      </sites>
        
      </xsl:for-each>


        <!-- <xsl:apply-templates select="item[generate-id() = generate-id(key('items-by-siteid', site_id)[1])]"/> -->
    </xsl:template>
   

   <xsl:template name='temp' match=" @* | node()">
         <xsl:copy>
               <xsl:apply-templates select="@* | node()" />
         </xsl:copy>
     </xsl:template>
</xsl:stylesheet>