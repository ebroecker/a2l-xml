<?xml version="1.0" encoding="iso-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:output method="text" />
 
<xsl:template match="/a2l">
	<xsl:apply-templates /> 
 <!-- xsl:value-of select="." / -->
</xsl:template>

<xsl:template match="PROJECT | MODULE | COMPU_METHOD | MEASUREMENT">
/begin <xsl:value-of select ="name(.)"/>
    <xsl:text> </xsl:text>
	<xsl:value-of select="@name"/> <xsl:choose><xsl:when test="@dimension">[<xsl:value-of select="@dim"/>]</xsl:when></xsl:choose> "<xsl:value-of select="@comment"/>"
 	<xsl:apply-templates /> 
/end <xsl:value-of select ="name(.)"/>
</xsl:template>

<xsl:template match="HEADER | MOD_COMMON | MOD_PAR">
  /begin <xsl:value-of select ="name(.)"/> "<xsl:value-of select="@comment"/>"
  <xsl:apply-templates /> 
  /end <xsl:value-of select ="name(.)"/>
</xsl:template>

<xsl:template match="IF_DATA">
  /begin <xsl:value-of select ="name(.)"/> 
  <xsl:text> </xsl:text> 
  <xsl:value-of select="@interface"/>
  <xsl:apply-templates /> 
  /end <xsl:value-of select ="name(.)"/>
</xsl:template>

<xsl:template match="A2ML | ANNOTATION | ANNOTATION_TEXT | PROTOCOL_LAYER | DAQ | PAQ | PAG | PGM | XCP_ON_TCP_IP | TIMESTAMP_SUPPORTED">
  /begin <xsl:value-of select ="name(.)"/> 
  <xsl:apply-templates /> 
  /end <xsl:value-of select ="name(.)"/>
</xsl:template>


<xsl:template match="ASAP2_VERSION">
  <xsl:value-of select ="name(.)"/> 
  <xsl:text> </xsl:text>
  <xsl:value-of select="@mayor"/>
  <xsl:text> </xsl:text>
  <xsl:value-of select="@minor"/>
  <xsl:text> </xsl:text>
</xsl:template>


<xsl:template match="struct|enum|taggedstruct|taggedunion">
  <xsl:value-of select ="name(.)"/>
  <xsl:text> </xsl:text>
  <xsl:value-of select="@name"/>
  <xsl:apply-templates name="block" /> 
</xsl:template>


<xsl:template match="list">
(  <xsl:apply-templates /> ) </xsl:template>


<xsl:template match="block"> { 
    <xsl:apply-templates /> 
}</xsl:template>

<xsl:template match="star">*</xsl:template>
<xsl:template match="equals">  "<xsl:value-of select="@lval"/>" = <xsl:value-of select="@rval"/>, 
</xsl:template>

<xsl:template match="var">
<xsl:choose><xsl:when test="@dim"><xsl:value-of select="@type"/>[<xsl:value-of select="@dim"/>]</xsl:when>
<xsl:otherwise><xsl:value-of select="@type"/></xsl:otherwise></xsl:choose>
</xsl:template>

<xsl:template match="string">  "<xsl:value-of select="@value"/>" </xsl:template>
<xsl:template match="item | keyword | datatype"> 
    <xsl:value-of select="@type"/> 
<xsl:text>
</xsl:text>
</xsl:template>

<xsl:template match="RECORD_LAYOUT">
  /begin <xsl:value-of select ="name(.)"/> 
  <xsl:text> </xsl:text>
  <xsl:value-of select="@name"/>
  <xsl:text> 
  </xsl:text>
  <xsl:value-of select="@type"/>
  <xsl:text> 
  </xsl:text>
  <xsl:value-of select="@val"/>
  <xsl:text> 
  </xsl:text>
  <xsl:value-of select="@basetype"/>
  <xsl:text> 
  </xsl:text>
  <xsl:value-of select="@col"/>
  <xsl:text> 
  </xsl:text>
  <xsl:value-of select="@direct"/>
  <xsl:text> </xsl:text>
  /end <xsl:value-of select ="name(.)"/>
</xsl:template>

<xsl:template match="semicol">;
</xsl:template>

<xsl:template match="*">
TODO: <xsl:value-of select ="name(.)"/><xsl:choose><xsl:when test="@dimension">[<xsl:value-of select="@dim"/>]</xsl:when></xsl:choose>
</xsl:template>

</xsl:stylesheet>

