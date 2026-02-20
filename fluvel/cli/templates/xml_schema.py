# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

XML_SCHEMA = """<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">

  <xs:complexType name="OptionType">
    <xs:simpleContent>
      <xs:extension base="xs:string">
        <xs:attribute name="id" type="xs:string" use="required"/>
        <xs:attribute name="icon" type="xs:string" use="optional"/>
        <xs:attribute name="checkable" type="xs:boolean" use="optional" default="false"/>
      </xs:extension>
    </xs:simpleContent>
  </xs:complexType>

  <xs:complexType name="SeparatorType"/>

  <xs:group name="MenuItemsGroup">
    <xs:choice>
      <xs:element name="o" type="OptionType"/>
      <xs:element name="sep" type="SeparatorType"/>
      <xs:element name="submenu" type="MenuContainerType"/>
      <xs:element name="menu" type="MenuContainerType"/>
    </xs:choice>
  </xs:group>

  <xs:complexType name="MenuContainerType">
    <xs:sequence>
      <xs:group ref="MenuItemsGroup" minOccurs="0" maxOccurs="unbounded"/>
    </xs:sequence>
    <xs:attribute name="id" type="xs:string" use="required"/>
    <xs:attribute name="text" type="xs:string" use="optional"/>
  </xs:complexType>

  <xs:element name="menu-structure">
    <xs:complexType>
      <xs:sequence>
        <xs:group ref="MenuItemsGroup" minOccurs="0" maxOccurs="unbounded"/>
      </xs:sequence>
    </xs:complexType>
  </xs:element>

</xs:schema>
"""