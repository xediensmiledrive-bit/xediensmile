"""Logo đầu trang có hiệu ứng "Sạc đầy pin" (~6 giây, chạy 1 lần khi mở trang).
Lấy font nhúng từ logo gốc, viết lại phần hình để từng ô pin chạy được."""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SET = '<path d="M13 0 1 14h7l-2 10 12-14h-7z"/>'
GIAM = "@media(prefers-reduced-motion:reduce){*{animation:none!important}}"


def _font(goc):
    s = open(goc, encoding="utf-8").read()
    return re.search(r"<style>(.*?)</style>", s, re.S).group(1)


def comvn(goc):
    o = "".join('<line class="o" style="animation-delay:%.2fs" x1="%d" y1="84" x2="%d" y2="84"/>' % (.6 + k * .32, 10 + 40 * k, 36 + 40 * k) for k in range(8))
    css = (".v{fill:none;stroke:#CFD6D2;stroke-width:2.5;opacity:0;animation:v 5.2s ease both}"
           ".o,.n{stroke:#6FD92E;stroke-width:7;stroke-linecap:round;animation:o .3s ease-out both}"
           ".n{animation-delay:3.1s}"
           ".s{fill:#FFE14D;opacity:0;transform-origin:162px 84px;animation:s 1.1s ease-out 3.2s both}"
           ".t{animation:t 1.4s ease-out 3.2s both}.c{animation:c .6s ease-out 4.2s both}"
           ".g{opacity:0;animation:g 1s ease-in-out 5s both}"
           "@keyframes v{0%{opacity:0}6%,80%{opacity:1}100%{opacity:0}}"
           "@keyframes o{from{stroke:#2B332E}to{stroke:#6FD92E}}"
           "@keyframes s{0%{opacity:0;transform:scale(0)}25%{opacity:1;transform:scale(1.3)}45%{transform:scale(1)}80%{opacity:1}100%{opacity:0}}"
           "@keyframes t{0%{fill:#3B4247}35%{fill:#fff;filter:drop-shadow(0 0 7px #6FD92E)}100%{fill:#fff}}"
           "@keyframes c{from{opacity:0}to{opacity:1}}"
           "@keyframes g{0%{opacity:0;transform:translateX(0)}10%,90%{opacity:1}100%{opacity:0;transform:translateX(420px)}}" + GIAM)
    chu = '<text x="6" y="64" font-family="Lexend" font-weight="800" font-size="50">Phố Xe Điện</text>'
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="2 10 332 110" width="332" height="110"><style>%s%s</style>'
            '<defs><clipPath id="k">%s</clipPath><linearGradient id="l" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".7"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>'
            '<g class="t" fill="#FFFFFF">%s</g>'
            '<g clip-path="url(#k)"><rect class="g" x="-90" y="10" width="70" height="60" fill="url(#l)" transform="skewX(-20)"/></g>'
            '<rect class="v" x="2.5" y="75.5" width="323" height="17" rx="5"/>%s<line class="n" x1="330" y1="84" x2="330" y2="84"/>'
            '<svg class="s" x="140" y="52" width="44" height="54" viewBox="0 0 20 24">%s</svg>'
            '<text class="c" x="8" y="112" font-family="Lexend" font-weight="600" font-size="14" fill="#A2ABB0" letter-spacing="4">CẨM NANG XE 50CC</text></svg>'
            % (_font(goc), css, chu, chu, o, SET))


def vn(goc):
    o = "".join('<rect class="o" style="animation-delay:%.2fs" x="%.1f" y="88" width="20" height="20" rx="5"/>' % (.6 + k * .5, 118 + 23.5 * k) for k in range(5))
    css = (".p{fill:#F26B1D;stroke:#F26B1D;stroke-width:3;animation:p .5s ease-out 3.2s both}"
           ".o{fill:#F26B1D;opacity:0;animation:o .35s ease-out both}.oo{animation:x .4s ease 3.4s both}"
           ".n{fill:#F26B1D;opacity:0;animation:v 5s ease both}"
           ".s{fill:#FFC21A;opacity:0;transform-origin:262px 90px;animation:s 1.1s ease-out 3.2s both}"
           ".t{animation:t 1.4s ease-out 3.2s both}.w{fill:#fff;animation:w .5s ease-out 3.5s both}"
           "@keyframes p{from{fill:#fff}to{fill:#F26B1D}}"
           "@keyframes o{from{opacity:0;transform:scaleY(.5)}to{opacity:1;transform:none}}"
           "@keyframes x{to{opacity:0}}"
           "@keyframes v{0%{opacity:0}6%,80%{opacity:1}100%{opacity:0}}"
           "@keyframes s{0%{opacity:0;transform:scale(0)}25%{opacity:1;transform:scale(1.3)}45%{transform:scale(1)}80%{opacity:1}100%{opacity:0}}"
           "@keyframes t{0%{opacity:.35}35%{opacity:1;filter:drop-shadow(0 0 6px #F26B1D)}100%{opacity:1}}"
           "@keyframes w{from{opacity:0}to{opacity:1}}" + GIAM)
    s = open(goc, encoding="utf-8").read()
    s = re.sub(r"<metadata>.*?</metadata>", "", s, flags=re.S)
    than = s[s.index("</style>") + 8:s.rindex("</svg>")]
    pin = re.search(r'<rect x="114"[^>]*/>', than).group(0)
    chu_smile = re.search(r'<text x="175".*?</text>', than).group(0)
    dau = than[:than.index(pin)]
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="2 9 281 107" width="281" height="107"><style>%s%s</style>'
            '<g class="t">%s</g>%s<g class="oo">%s</g><rect class="n" x="238" y="92" width="5" height="12" rx="2"/>%s'
            '<svg class="s" x="249" y="74" width="26" height="32" viewBox="0 0 20 24">%s</svg></svg>'
            % (_font(goc), css, dau, pin.replace("<rect ", '<rect class="p" '), o,
               chu_smile.replace("<text ", '<text class="w" ').replace('fill="#fff" ', ""), SET))


def ghi(out_dir, domain):
    thu = os.path.join(HERE, "logo", domain)
    if domain == "phoxedien.com.vn":
        svg = comvn(os.path.join(thu, "logo-nen-toi.svg"))
    elif domain == "phoxedien.vn":
        svg = vn(os.path.join(thu, "logo.svg"))
    else:
        return False
    open(os.path.join(out_dir, "logo-dong.svg"), "w", encoding="utf-8").write(svg)
    return True


if __name__ == "__main__":
    import sys
    for d in ("phoxedien.com.vn", "phoxedien.vn"):
        os.makedirs(os.path.join(sys.argv[1], d), exist_ok=True)
        ghi(os.path.join(sys.argv[1], d), d)
