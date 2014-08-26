<h1>API and Frontend for Longest Increasing Subsequence</h1>
<p>The code in this directory creates the website found at
<a href="http://54.84.243.150/">http://54.84.243.150/</a></p>

<p>It consists of two parts, a REST API call, and a web interface.</p>

<h2>REST API call</h2>

<p>The REST API call takes as input a sequence of integers, and outputs the longest increasing subsequence within that sequence of integers. There is an optional <code>verbose</code> parameter which allows you to receive a list of indexes of the longest increasing subsequence numbers within the original sequence, along with runtime information.</p>

<p>An example API call is:</p>

<code>curl -H "Content-Type: application/json" -X POST -d '{"num_array":"1,4,5,6,2,1,5,7,3","verbose":1}' http://54.84.243.150/api/longest/</code>

<p>and the resulting JSON output is</p>

<code>{"indexes": "0,1,2,3,7", "time": "3.2901763916e-05", "out": "1,4,5,6,7"}</code>

<p>If called without the <code>verbose</code> parameter (or with <code>"verbose":0</code> or <code>"verbose":false</code>), then the call and output is simply:</p>

<code>curl -H "Content-Type: application/json" -X POST -d '{"num_array":"1,4,5,6,2,1,5,7,3"}' http://54.84.243.150/api/longest/</code>

<p>and the resulting JSON output is</p>

<code>{"out": "1,4,5,6,7"}</code>

<h5>Error Codes</h5>

<p>If the API encounters an error in the incoming POST request, then an error is output in JSON. The data format for "num_array" is flexible enough to handle arbitrary amounts of spaces, but certain mistakes will trigger an error, such as a non-integer value. Some example errors are:</p>

<p>A non-POST request</p>
<code>{"error":"Only method 'POST' is allowed"}</code>

<p>Improperly formatted JSON in request<p>
<code>{"error":"Request data not properly formatted"}</code>

<p>If "num_array" was not defined in JSON</p>
<code>{"error":"'num_array' not specified"}</code>

<p>More than 1,000 numbers are in "num_array"</p>
<code>{"error":"Input numbers are limited to 1,000 values"}</code>

<p>A non-integer value is found in "num_array"</p>
<code>{"error":"Input numbers do not contain valid values"}</code>

<p>An integer value is out of range of a Python integer (-2^63 to 2^63-1)</p>
<code>{"error":"Input numbers should only contain integer values (-9223372036854775808 to 9223372036854775807)"}</code>

<h4>Algorithm</h4>

<p>The algorithm which powers the API is found in the file</p>

<a href="https://github.com/Estherbunny/LongestSubsequence/blob/master/sequence/sequence/views.py">/sequence/sequence/views.py</a>

<p>It is an <i>O (n log n)</i> implementation of finding the longest increasing subsequence. It is easy to see that there exists an <i>O (n^2)</i> solution to the problem of finding the longest increasing subsequence in an input sequence <i>x<sub>0</sub>,x<sub>1</sub>,...x<sub>n-1</sub></i>. First, let's present that.</p>

<p>Let <i>L(i)</i> represent the longest increasing subsequence at index <i>i</i> of our input sequence. Then <i>L(i)=0</i> if <i>i=0</i>, and <i>L(i) = 1 + max<sub>j=0,...,(i-1)</sub>L(j)</i> if <i>x<sub>j</sub> &lt; x<sub>i</sub></i> and <i>i>0</i>. One can then use dynamic programming to create an array of size <i>n</i> which stores <i>L(i)</i>, and then for each <i>i</i>, traversed in order, the values of all <i>L(j)</i> and <i>x<sub>j</sub></i> (where <i>j &lt; i</i>) can be used to determine the value of <i>L(i)</i>.  This traversal of up to <i>n</i> previous data points, for each of the <i>n</i> data points gives rise to an <i>O (n^2)</i> runtime.</p>

<p>As we traverse the <i>j = 0,1,...,(i-1)</i> elements in for every <i>i</i>, it should become apparent that we are only interested in some "best case" <i>x<sub>j</sub></i>, and all <i>j</i> that are not these "best case" scenarios are irrelevant. When we are calculating <i>L(i)</i>, we search to extend a subsequence of length <i>m</i>, where <i>0 &le; m &le; M</i>, and <i>M</i> is the length of the largest subsequence found thus far. For every <i>m</i>, there is some <i>x<sub>j</sub></i> which is the smallest integer value that is the final data point in that subsequence of size <i>m</i>. We always want to extend the maximum <i>m</i> possible to get the longest subsequence, while still making sure that <i>x<sub>i</sub> &gt; x<sub>j</sub></i> for the <i>x<sub>j</sub></i> corresponding to that <i>m</i>.</p>

<p>We introduce a new variable <i>S(m)</i> which is the index of the largest datapoint that forms the subsequence of length <i>m</i>, where <i>0 &le; m &le; M</i>. Note that as we traverse the input sequence from <i>i = 0,1,...,(n-1)</i>, the value of <i>S(m)</i> will change, and <i>M</i> will also grow from <i>M=0</i> to the eventual length of the longest increasing subsequence. We make the observation that <i>x<sub>S(m)</sub> &lt; x<sub>S(m+1)</sub></i>. This has to be true, since if <i>x<sub>S(m+1)</sub> &lt; x<sub>S(m)</sub></i>, then it would mean that there exists some smaller value which should have been <i>x<sub>S(m)</sub></i>. Since <i>x<sub>S(m)</sub> &lt; x<sub>S(m+1)</sub></i>, then finding the largest subsequence, <i>m</i> for a new value <i>x<sub>i</sub></i>, is only a matter of finding where its place is in the ordered sequence <i>x<sub>S(0)</sub>,x<sub>S(1)</sub>,...,x<sub>S(M)</sub></i>. If <i>x<sub>i</sub></i> is in fact larger than <i>x<sub>S(M)</sub></i>, then a new value for <i>M</i> is found and <i>S</i> is expanded. If <i>m</i> is identified as the insertion point for <i>x<sub>i</sub>, and <i>x<sub>i</sub> &lt; x<sub>S(m)</sub></i>, then <i>S(m)</i> is updated to the index <i>i</i>.</p>

<p>Because the list <i>x<sub>S(0)</sub>,x<sub>S(1)</sub>,...,x<sub>S(M)</sub></i> is sorted, locating an insertion point is possible in <i>O (log n)</i> using binary search. Since we do this for every <i>i</i>, where <i>i = 0,1,...,(n-1)</i>, the entire algorithm takes <i>O (n log n)</i> to run.</p>

<h2>Web Frontend</h2>

<p>The web frontend is powered by a <a href="https://github.com/Estherbunny/LongestSubsequence/blob/master/templates/frontend/home.html">template file</a>, <a href="https://github.com/Estherbunny/LongestSubsequence/blob/master/sequence/frontend/views.py">views.py file</a>, and <a href="https://github.com/Estherbunny/LongestSubsequence/blob/master/sequence/frontend/models.py">models.py file</a>.</p>

<p>In the <a href="https://github.com/Estherbunny/LongestSubsequence/blob/master/templates/frontend/home.html">template file</a>, the open source Javascript library <a href="http://www.jqplot.com/index.php">jqPlot</a> was used to make  graphs of the input numbers and the resulting longest increasing subsequence. Random numbers can be generated using Javascript.</p>

<p>In the <a href="https://github.com/Estherbunny/LongestSubsequence/blob/master/sequence/frontend/views.py">views.py file</a>, a call is made to the API using Python's <code>urllib2</code> library. The output and indexes are formated for the template.</p>

<p>In the <a href="https://github.com/Estherbunny/LongestSubsequence/blob/master/sequence/frontend/models.py">models.py file</a>, the form NumberForm() is defined. This form accepts the user's input on the main page</p>

<h2>Directory Structure</h2>

<p>The directory structure for the website and the API are as follows:</p>

<p>
<code>/static/</code><br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>css/</code> : contains all CSS files (bootstrap3 and JQuery)<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>js/</code> : contains all JS files (JQuery and jqPlot)<br />
<br />
<code>/templates/</code><br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>frontend/</code><br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>home.html</code> : template file for the homepage<br />
<br />
<code>/sequence/</code><br />
</p>






