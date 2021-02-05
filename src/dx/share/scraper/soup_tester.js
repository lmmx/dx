all_descs = []
function allDescendants (node) {
    all_descs.push(node.tagName.toLowerCase());
    for (var i = 0; i < node.childElementCount; i++) {
        var child = node.childElements()[i];
        allDescendants(child);
    }
}
allDescendants(document.querySelector("html"))
console.log(all_descs.length)

set_descs = new Set(all_descs)
arr_uniq_descs = Array.from(set_descs)

// build a count dictionary

var k_count_dict = Object.fromEntries(arr_uniq_descs.map(function(x){return [x, 0]}));
for (var k_i = 0; k_i < arr_uniq_descs.length; k_i++){
    var k = arr_uniq_descs[k_i];
    var k_count = 0;
    for (var n_i = 0; n_i < all_descs.length; n_i++) {
        if (all_descs[n_i] == k) {
            k_count++;
        }
    }
    k_count_dict[k] = k_count;
}

kc_str = "";
for (const [key, value] of Object.entries(k_count_dict)){
    kc_str += key + ", " + value + "\n";
}

/* a, 82
 * b, 1
 * body, 1
 * br, 28
 * button, 2
 * div, 115
 * em, 2
 * footer, 1
 * form, 3
 * h1, 2
 * h2, 8
 * h3, 2
 * h4, 3
 * head, 1
 * hr, 2
 * html, 1 // there are 2 htmls in BeautifulSoup (due to the iframe?)
 * i, 3
 * img, 6 // there is an iframe in BeautifulSoup
 * input, 9
 * label, 2
 * li, 58
 * link, 14
 * meta, 5
 * noscript, 1
 * option, 4
 * p, 27
 * script, 37  // this is 33 in BeautifulSoup (XSS)
 * select, 1
 * span, 268
 * strong, 6
 * style, 9 // this is 2 in BeautifulSoup (XSS)
 * sup, 1
 * table, 1
 * tbody, 1
 * td, 2
 * title, 1
 * tr, 2
 * ul, 18
 */
