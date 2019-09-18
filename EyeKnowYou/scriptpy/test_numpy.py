import execnet

class TestNumpy :
    def __init__(self, file_path=None):
        self.file_path = file_path

    def test_np(self):  

        gw = execnet.makegateway("popen//python=python")
        channel = gw.remote_exec("""
            from numpy import *
            a = array([2,3,4])
            channel.send(a.size)
        """)

        for item in channel:
            print item