function addProductToOrder(productId) {
    var productCount = 1;
    $.get('/user-panel/add-to-order?product_id=' + productId + '&count=' + productCount).then(res => {
        Swal.fire({
            title: 'Alert',
            text: res.text,
            icon: res.icon,
            showCancelButton: false,
            confirmButtonColor: '#e2c743',
            confirmButtonText: res.confirm_button_text
        });
    });
}

function changeOrderDetailCount(detailId, state) {
    location.reload();
    $.get('/user-panel/change-order-detail?detail_id=' + detailId + '&state=' + state).then(res => {
        if (res.status === 'success') {
            $('#order-detail-content').html(res.body);
        }
    });
}


