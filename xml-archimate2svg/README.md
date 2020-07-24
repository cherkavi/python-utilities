![schema](https://i.postimg.cc/gr9RvCZ6/archimate-enrichment-from-properties.png)

Archimate to SVG export improvement.
Update destination SVG with all links from documentation properties ( also add popup hints to elements)


example of 
```html
<g>
        <a onclick='showTooltip(event)' data-doc="doc:https://asc.ubsgroup.net/wiki/display/Developer+Manual+Automatic+Labeling | readme: https://asc.ubsgroup.net/wiki/display/Developer+Manual+Automatic+Labeling" >
            <text>some text</text>
        </a>

        <rect id="tooltip" x="100" y="100" width="70" height="40" 
              style="fill:rgb(255,255,0);display: none"
              onclick='hideTooltip()'>
              <title>some text</title>
        </rect>

</g>
<script type="text/ecmascript">
<![CDATA[
alert("script!!!");
]]>
</script>
```
        