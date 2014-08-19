import json

class TargetState:
    _m_status = ""
    _m_targetId = ""
    _m_activeFlag = False
    _m_name = ""
    _m_width = 0.0
    _m_trackingRating = 0
    _m_recoRating = ""

    _hasState = False

    @property
    def m_status(self):
        return self._m_status

    @m_status.setter
    def m_status(self, m_status):
        self._m_status = m_status

    @property
    def m_targetId(self):
        return self._m_targetId

    @m_targetId.setter
    def m_targetId(self, m_targetId):
        self._m_targetId = m_targetId

    @property
    def m_activeFlag(self):
        return self._m_activeFlag

    @m_activeFlag.setter
    def m_activeFlag(self, m_activeFlag):
        self._m_activeFlag = m_activeFlag

    @property
    def m_name(self):
        return self._name

    @m_name.setter
    def m_name(self, m_name):
        self._m_name = m_name

    @property
    def m_width(self):
        return self._m_width

    @m_width.setter
    def m_width(self, m_width):
        self._m_width = m_width

    @property
    def m_trackingRating(self):
        return self._m_trackingRating

    @m_trackingRating.setter
    def m_trackingRating(self, m_trackingRating):
        self._m_trackingRating = m_trackingRating

    @property
    def m_recoRating(self):
        return self._m_recoRating

    @m_recoRating.setter
    def m_recoRating(self, m_recoRating):
        self._m_recoRating = m_recoRating

    @staticmethod
    def createFromJSON(jobj):
        if (jobj == None):
            raise ValueError("Failed to create TargetState from JSON object: JSON object may not be null!")

        result = TargetState()
        result.hasState = True

        jobj = json.loads(jobj)

        try:
            result.m_status = jobj["status"]
            result.m_targetId = jobj["target_record"]["target_id"]

            # not mandatory
            if ( jobj["target_record"].has_key("active_flag" ) ):
                result.m_activeFlag = jobj["target_record"]["active_flag"]

            result.m_name = jobj["target_record"]["name"]
            result.m_width = (float) (jobj["target_record"]["width"])
            result.m_trackingRating = jobj["target_record"]["tracking_rating"]

            # not mandatory
            if ( jobj["target_record"].has_key("reco_rating") ):
                result.m_recoRating = jobj["target_record"]["reco_rating"]
        except Exception as e:
            print "Error creating TargetState: " + str(e)
            return None

        return result

