<html>
<head>
<title>book.js</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<style type="text/css">
.s0 { color: #7a7e85;}
.s1 { color: #bcbec4;}
.s2 { color: #bcbec4;}
.s3 { color: #6aab73;}
.s4 { color: #cf8e6d;}
.s5 { color: #2aacb8;}
</style>
</head>
<body bgcolor="#1e1f22">
<table CELLSPACING=0 CELLPADDING=5 COLS=1 WIDTH="100%" BGCOLOR="#606060" >
<tr><td><center>
<font face="Arial, Helvetica" color="#000000">
book.js</font>
</center></td></tr></table>
<pre><span class="s0">// Simple interactivity for time slots</span>
<span class="s1">document</span><span class="s2">.</span><span class="s1">querySelectorAll</span><span class="s2">(</span><span class="s3">'.time-slot'</span><span class="s2">).</span><span class="s1">forEach</span><span class="s2">(</span><span class="s1">slot </span><span class="s2">=&gt; {</span>
  <span class="s1">slot</span><span class="s2">.</span><span class="s1">addEventListener</span><span class="s2">(</span><span class="s3">'click'</span><span class="s2">, () =&gt; {</span>
    <span class="s1">document</span><span class="s2">.</span><span class="s1">querySelectorAll</span><span class="s2">(</span><span class="s3">'.time-slot'</span><span class="s2">).</span><span class="s1">forEach</span><span class="s2">(</span><span class="s1">s </span><span class="s2">=&gt; {</span>
      <span class="s1">s</span><span class="s2">.</span><span class="s1">classList</span><span class="s2">.</span><span class="s1">remove</span><span class="s2">(</span><span class="s3">'selected'</span><span class="s2">);</span>
    <span class="s2">});</span>
    <span class="s1">slot</span><span class="s2">.</span><span class="s1">classList</span><span class="s2">.</span><span class="s1">add</span><span class="s2">(</span><span class="s3">'selected'</span><span class="s2">);</span>
  <span class="s2">});</span>
<span class="s2">});</span>

<span class="s0">// Guest counter functionality</span>
<span class="s4">const </span><span class="s1">minusBtn </span><span class="s2">= </span><span class="s1">document</span><span class="s2">.</span><span class="s1">querySelector</span><span class="s2">(</span><span class="s3">'.counter-btn:first-child'</span><span class="s2">);</span>
<span class="s4">const </span><span class="s1">plusBtn </span><span class="s2">= </span><span class="s1">document</span><span class="s2">.</span><span class="s1">querySelector</span><span class="s2">(</span><span class="s3">'.counter-btn:last-child'</span><span class="s2">);</span>
<span class="s4">const </span><span class="s1">counterValue </span><span class="s2">= </span><span class="s1">document</span><span class="s2">.</span><span class="s1">querySelector</span><span class="s2">(</span><span class="s3">'.counter-value'</span><span class="s2">);</span>

<span class="s1">minusBtn</span><span class="s2">.</span><span class="s1">addEventListener</span><span class="s2">(</span><span class="s3">'click'</span><span class="s2">, () =&gt; {</span>
  <span class="s4">let </span><span class="s1">value </span><span class="s2">= </span><span class="s1">parseInt</span><span class="s2">(</span><span class="s1">counterValue</span><span class="s2">.</span><span class="s1">textContent</span><span class="s2">);</span>
  <span class="s4">if </span><span class="s2">(</span><span class="s1">value </span><span class="s2">&gt; </span><span class="s5">1</span><span class="s2">) {</span>
    <span class="s1">counterValue</span><span class="s2">.</span><span class="s1">textContent </span><span class="s2">= </span><span class="s1">value </span><span class="s2">- </span><span class="s5">1</span><span class="s2">;</span>
  <span class="s2">}</span>
<span class="s2">});</span>

<span class="s1">plusBtn</span><span class="s2">.</span><span class="s1">addEventListener</span><span class="s2">(</span><span class="s3">'click'</span><span class="s2">, () =&gt; {</span>
  <span class="s4">let </span><span class="s1">value </span><span class="s2">= </span><span class="s1">parseInt</span><span class="s2">(</span><span class="s1">counterValue</span><span class="s2">.</span><span class="s1">textContent</span><span class="s2">);</span>
  <span class="s4">if </span><span class="s2">(</span><span class="s1">value </span><span class="s2">&lt; </span><span class="s5">12</span><span class="s2">) {</span>
    <span class="s1">counterValue</span><span class="s2">.</span><span class="s1">textContent </span><span class="s2">= </span><span class="s1">value </span><span class="s2">+ </span><span class="s5">1</span><span class="s2">;</span>
  <span class="s2">}</span>
<span class="s2">});</span>

<span class="s0">// Set default date to today</span>
<span class="s4">const </span><span class="s1">today </span><span class="s2">= </span><span class="s4">new </span><span class="s1">Date</span><span class="s2">();</span>
<span class="s4">const </span><span class="s1">formattedDate </span><span class="s2">= </span><span class="s1">today</span><span class="s2">.</span><span class="s1">toISOString</span><span class="s2">().</span><span class="s1">split</span><span class="s2">(</span><span class="s3">'T'</span><span class="s2">)[</span><span class="s5">0</span><span class="s2">];</span>
<span class="s1">document</span><span class="s2">.</span><span class="s1">getElementById</span><span class="s2">(</span><span class="s3">'reservation-date'</span><span class="s2">).</span><span class="s1">value </span><span class="s2">= </span><span class="s1">formattedDate</span><span class="s2">;</span>

<span class="s0">// Navigation anchors</span>
<span class="s1">document</span><span class="s2">.</span><span class="s1">querySelectorAll</span><span class="s2">(</span><span class="s3">'.nav-link'</span><span class="s2">).</span><span class="s1">forEach</span><span class="s2">(</span><span class="s1">link </span><span class="s2">=&gt; {</span>
  <span class="s1">link</span><span class="s2">.</span><span class="s1">addEventListener</span><span class="s2">(</span><span class="s3">'click'</span><span class="s2">, </span><span class="s4">function</span><span class="s2">(</span><span class="s1">e</span><span class="s2">) {</span>
    <span class="s1">e</span><span class="s2">.</span><span class="s1">preventDefault</span><span class="s2">();</span>

    <span class="s0">// Remove active class from all links</span>
    <span class="s1">document</span><span class="s2">.</span><span class="s1">querySelectorAll</span><span class="s2">(</span><span class="s3">'.nav-link'</span><span class="s2">).</span><span class="s1">forEach</span><span class="s2">(</span><span class="s1">l </span><span class="s2">=&gt; {</span>
      <span class="s1">l</span><span class="s2">.</span><span class="s1">classList</span><span class="s2">.</span><span class="s1">remove</span><span class="s2">(</span><span class="s3">'active'</span><span class="s2">);</span>
    <span class="s2">});</span>

    <span class="s0">// Add active class to clicked link</span>
    <span class="s4">this</span><span class="s2">.</span><span class="s1">classList</span><span class="s2">.</span><span class="s1">add</span><span class="s2">(</span><span class="s3">'active'</span><span class="s2">);</span>

    <span class="s0">// For demonstration purposes, we'll just scroll to different sections</span>
    <span class="s0">// In a real implementation, these would navigate to different sections/tabs</span>
    <span class="s4">const </span><span class="s1">targetId </span><span class="s2">= </span><span class="s4">this</span><span class="s2">.</span><span class="s1">getAttribute</span><span class="s2">(</span><span class="s3">'href'</span><span class="s2">).</span><span class="s1">substring</span><span class="s2">(</span><span class="s5">1</span><span class="s2">);</span>

    <span class="s0">// Show which section was clicked (for demo)</span>
    <span class="s1">console</span><span class="s2">.</span><span class="s1">log</span><span class="s2">(</span><span class="s3">`Navigating to section: </span><span class="s1">$</span><span class="s2">{</span><span class="s1">targetId</span><span class="s2">}</span><span class="s3">`</span><span class="s2">);</span>
  <span class="s2">});</span>
<span class="s2">});</span>

<span class="s0">// Book Table button functionality</span>
<span class="s1">document</span><span class="s2">.</span><span class="s1">getElementById</span><span class="s2">(</span><span class="s3">'book-table-btn'</span><span class="s2">).</span><span class="s1">addEventListener</span><span class="s2">(</span><span class="s3">'click'</span><span class="s2">, </span><span class="s4">function</span><span class="s2">() {</span>
  <span class="s0">// Get form values</span>
  <span class="s4">const </span><span class="s1">date </span><span class="s2">= </span><span class="s1">document</span><span class="s2">.</span><span class="s1">getElementById</span><span class="s2">(</span><span class="s3">'reservation-date'</span><span class="s2">).</span><span class="s1">value</span><span class="s2">;</span>
  <span class="s4">const </span><span class="s1">timeSelect </span><span class="s2">= </span><span class="s1">document</span><span class="s2">.</span><span class="s1">getElementById</span><span class="s2">(</span><span class="s3">'reservation-time'</span><span class="s2">);</span>
  <span class="s4">const </span><span class="s1">time </span><span class="s2">= </span><span class="s1">timeSelect</span><span class="s2">.</span><span class="s1">options</span><span class="s2">[</span><span class="s1">timeSelect</span><span class="s2">.</span><span class="s1">selectedIndex</span><span class="s2">].</span><span class="s1">text</span><span class="s2">;</span>
  <span class="s4">const </span><span class="s1">guests </span><span class="s2">= </span><span class="s1">document</span><span class="s2">.</span><span class="s1">querySelector</span><span class="s2">(</span><span class="s3">'.counter-value'</span><span class="s2">).</span><span class="s1">textContent</span><span class="s2">;</span>

  <span class="s0">// Get customer information</span>
  <span class="s4">const </span><span class="s1">nameInput </span><span class="s2">= </span><span class="s1">document</span><span class="s2">.</span><span class="s1">querySelector</span><span class="s2">(</span><span class="s3">'.form-group:nth-of-type(3) input'</span><span class="s2">);</span>
  <span class="s4">const </span><span class="s1">phoneInput </span><span class="s2">= </span><span class="s1">document</span><span class="s2">.</span><span class="s1">querySelector</span><span class="s2">(</span><span class="s3">'.phone-input'</span><span class="s2">);</span>
  <span class="s4">const </span><span class="s1">emailInput </span><span class="s2">= </span><span class="s1">document</span><span class="s2">.</span><span class="s1">querySelector</span><span class="s2">(</span><span class="s3">'input[type=&quot;email&quot;]'</span><span class="s2">);</span>
  <span class="s4">const </span><span class="s1">requestsInput </span><span class="s2">= </span><span class="s1">document</span><span class="s2">.</span><span class="s1">querySelector</span><span class="s2">(</span><span class="s3">'.form-group:nth-of-type(8) input'</span><span class="s2">);</span>

  <span class="s0">// Create URL with parameters</span>
  <span class="s4">const </span><span class="s1">url </span><span class="s2">= </span><span class="s3">`confirmation.html?date=</span><span class="s1">$</span><span class="s2">{</span><span class="s1">date</span><span class="s2">}</span><span class="s3">&amp;time=</span><span class="s1">$</span><span class="s2">{</span><span class="s1">time</span><span class="s2">}</span><span class="s3">&amp;guests=</span><span class="s1">$</span><span class="s2">{</span><span class="s1">guests</span><span class="s2">}</span><span class="s3">&amp;name=</span><span class="s1">$</span><span class="s2">{</span><span class="s1">nameInput</span><span class="s2">.</span><span class="s1">value</span><span class="s2">}</span><span class="s3">&amp;phone=</span><span class="s1">$</span><span class="s2">{</span><span class="s1">phoneInput</span><span class="s2">.</span><span class="s1">value</span><span class="s2">}</span><span class="s3">&amp;email=</span><span class="s1">$</span><span class="s2">{</span><span class="s1">emailInput</span><span class="s2">.</span><span class="s1">value</span><span class="s2">}</span><span class="s3">&amp;requests=</span><span class="s1">$</span><span class="s2">{</span><span class="s1">requestsInput</span><span class="s2">.</span><span class="s1">value</span><span class="s2">}</span><span class="s3">`</span><span class="s2">;</span>

  <span class="s0">// Redirect to confirmation page</span>
  <span class="s1">window</span><span class="s2">.</span><span class="s1">location</span><span class="s2">.</span><span class="s1">href </span><span class="s2">= </span><span class="s1">url</span><span class="s2">;</span>
<span class="s2">});</span></pre>
</body>
</html>