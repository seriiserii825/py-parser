class Utils:
    @staticmethod
    def replaceByArray(text, arr):
        for item in arr:
            text = text.replace(item, "_")
        return text
