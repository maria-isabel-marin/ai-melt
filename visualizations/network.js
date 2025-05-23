
function downloadImage() {
    var container = document.getElementById('mynetwork');
    html2canvas(container, {useCORS: true, logging: true}).then(function(canvas) {
        var link = document.createElement('a');
        link.href = canvas.toDataURL('image/png');
        link.download = 'network_graph.png';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });
}

function searchNode() {
    var nodeId = document.getElementById('searchNode').value;
    var options = {
        scale: 1.5,
        offset: {x:0, y:0},
        animation: {
            duration: 1000,
            easingFunction: 'easeInOutQuad'
        }
    };
    network.focus(nodeId, options);
    network.selectNodes([nodeId]);
}
