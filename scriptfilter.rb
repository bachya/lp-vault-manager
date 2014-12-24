# Creates a Script Filter item block.
# @param [String] uid
# @param [String] arg
# @param [String] title
# @param [String] subtitle
# @return [String]
def scriptfilter_block(uid, arg, title, subtitle)
  template = <<-XMLTEMPLATE
  <item uid="<%= uid %>" arg="<%= arg %>">
    <title><%= title %></title>
    <subtitle><%= subtitle %></subtitle>
  </item>
  XMLTEMPLATE
  ERB.new(template).result(binding)
end

# Creates a Script Filter XML document
# by using a block to fill its contents.
# @yield if block is present
# @return [String]
def scriptfilter_xml
  template = <<-XML
<?xml version="1.0"?>
<items>
<%= yield if block_given? %>
</items>
  XML
  ERB.new(template).result(binding)
end

