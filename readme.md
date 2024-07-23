<form method="post" action="https://test.yenepay.com/"> 
        <input type="hidden" name="Process" value="Express"> 
        <!--A unique identifier for the payment order. Yenepay will attach it to the order and echo it back when sending you any inforamtion about the order. To let the customer complete unfinished order you can send it again with the same order info--> 
        <input type="hidden" name="MerchantOrderId" value="{{product.orderid}}"> 
        <!--Your yenepay merchant code--> 
        <input type="hidden" name="MerchantId" value="SB2551"> 
        <!-- The ipn url that you want yenepay to send you ipn messages to. Note localhost is not accepted here--> 
        <input type="hidden" name="IPNUrl" value=""> 
        <!-- The url in your website or application that you want yenepay to redirect the customer after completing their payment. Note localhost is not accepted here--> 
        <input type="hidden" name="SuccessUrl" value="https://sandbox.yenepay.com/Home/Details/73110e4c-5aec-401f-a79f-1128a023f8ed?custId=d655d940-58b4-4b81-a3dc-e80cfbf4fa75"> 
        <!-- The url in your website or application that you want yenepay to redirect the customer when canceling their payment. Note localhost is not accepted here--> 
        <input type="hidden" name="CancelUrl" value="https://sandbox.yenepay.com/Home/Details/73110e4c-5aec-401f-a79f-1128a023f8ed?custId=d655d940-58b4-4b81-a3dc-e80cfbf4fa75"> 
        <!--A unique identifier for each item in the order. You can leave this blank if you want too.--> 
        <input type="hidden" name="ItemId" value="{{product.id}}"> 
        <!--The name for the item that that your customer is paying for--> 
        <input type="hidden" name="ItemName" value="{{product.name}}"> 
        <!--The unit price for the item this must be a positive decimal number and can not be empty or zero--> 
        <input type="hidden" name="UnitPrice" value="{{product.price}}"> 
        <!--The quantity for the item this must be a positive integer number with minimum value of 1--> 
        <!--The total price for the item will be determined by multiplying UnitPrice x Quantity for the item--> 
        <input type="hidden" name="Quantity" value="1"> 
        <!--Submit button--> 
        <input type="submit" class="btn btn-gray btn-block mb-2" value="Buy With YenePay"> 
    </form>