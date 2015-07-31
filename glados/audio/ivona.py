from pyvona import Voice, PyvonaException


class Ivona(Voice):

    def fetch_voice_fp(self, text_to_speak, f):
        """Fetch a voice file for given text and save it to the given file name
        """
        r = self._send_amazon_auth_packet_v4(
            'POST', 'tts', 'application/json', '/CreateSpeech', '',
            self._generate_payload(text_to_speak), self._region, self._host)
        if r.content.startswith(b'{'):
            raise PyvonaException('Error fetching voice: {}'.format(r.content))
        else:

            f.write(r.content)
