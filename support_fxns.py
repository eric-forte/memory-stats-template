def test_fxn():
    import time
    my_dict = {"x":0}
    # in async sleep freezes resources 
    time.sleep(1)
    return 0