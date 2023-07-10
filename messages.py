def amazon_msg(name, price, discount):

    # Amazon Message
    return f'''
    ---------------------------------------------------------------------------------

    (Amazon)

    Name      =>  {name}

    Price     =>  {price}

    Discount  =>  {discount[1:]}

    ----------------------------------------------------------------------------------

    '''


def flipkart_msg(name, price, discount, status, link, curr_time):

    # Flipkart Message
    return f'''

(Flipkart)  at  {curr_time}

Name      =>  {name}

Price     =>  {price}

Discount  =>  {discount}

Status    =>  {status}


Link      =>  {link}  

    '''



